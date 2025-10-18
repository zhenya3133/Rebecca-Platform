import uuid
from typing import Any, Dict

from fastapi import Body, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from orchestrator.main_workflow import main_workflow
from platform_logger import log_event
from core_adapter import CoreConfig, RebeccaCoreAdapter


app = FastAPI()

API_TOKEN = "supersecrettoken"  # TODO: поменять на свой
CORE_CONFIG: CoreConfig
CORE_ADAPTER: RebeccaCoreAdapter


class CoreSettingsPayload(BaseModel):
    endpoint: str
    auth_token: str
    transport: str = "grpc"
    timeout_seconds: int = 30
    llm_default: str = "creative"
    llm_fallback: str = "default"
    stt_engine: str = "whisper"
    tts_engine: str = "edge"
    ingest_pipeline: str = "auto"


def reload_core_adapter(config: CoreConfig | None = None) -> None:
    global CORE_CONFIG, CORE_ADAPTER  # noqa: PLW0603
    CORE_CONFIG = config or CoreConfig.load()
    CORE_ADAPTER = RebeccaCoreAdapter.from_config(CORE_CONFIG)


def _require_api_token(authorization: str | None) -> None:
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid token")


reload_core_adapter()


@app.post("/run")
async def run_pipeline(request: Request, authorization: str = Header(None)):
    _require_api_token(authorization)

    data = await request.json()
    input_data = data.get("input_data", "")
    trace_id = data.get("trace_id", str(uuid.uuid4()))
    log_event(f"API Call: trace_id={trace_id}, input_data={input_data}, token={authorization}")
    context_envelope = CORE_ADAPTER.fetch_context(trace_id)
    result = main_workflow(input_data)
    CORE_ADAPTER.emit_event("workflow.completed", {"trace_id": trace_id})
    log_event(f"API Result: trace_id={trace_id}, result={result.get('result', '')}")
    return {"result": result, "trace_id": trace_id, "context": context_envelope}


@app.get("/health")
async def health_check() -> JSONResponse:
    ok = CORE_ADAPTER.connectivity_check()
    status = {"status": "ok" if ok else "degraded"}
    return JSONResponse(content=status, status_code=200 if ok else 503)


@app.get("/core-settings")
async def get_core_settings(authorization: str = Header(None)) -> Dict[str, Any]:
    _require_api_token(authorization)
    config = CoreConfig.load()
    return config.to_dict()


@app.put("/core-settings")
async def update_core_settings(
    payload: CoreSettingsPayload = Body(...),
    authorization: str = Header(None),
) -> Dict[str, Any]:
    _require_api_token(authorization)
    config = CoreConfig.load()
    config.endpoint = payload.endpoint
    config.auth_token = payload.auth_token
    config.transport = payload.transport
    config.timeout_seconds = payload.timeout_seconds
    config.llm_default = payload.llm_default
    config.llm_fallback = payload.llm_fallback
    config.stt_engine = payload.stt_engine
    config.tts_engine = payload.tts_engine
    config.ingest_pipeline = payload.ingest_pipeline
    config.save()
    reload_core_adapter(config)
    return config.to_dict()

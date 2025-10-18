import uuid
from typing import Any, Dict

from fastapi import Body, FastAPI, File, Header, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from orchestrator.main_workflow import main_workflow
from platform_logger import log_event
from core_adapter import CoreConfig, RebeccaCoreAdapter
from memory_manager import memory_manager
from ingest.loader import IngestPipeline
from storage.pg_dao import InMemoryDAO
from storage.object_store import InMemoryObjectStore
from storage.graph_view import InMemoryGraphView
from retrieval.indexes import InMemoryBM25Index, InMemoryVectorIndex, InMemoryGraphIndex
from event_graph.event_graph import InMemoryEventGraph


app = FastAPI()

API_TOKEN = "supersecrettoken"  # TODO: поменять на свой
CORE_CONFIG: CoreConfig
CORE_ADAPTER: RebeccaCoreAdapter
DOCUMENT_STORE = InMemoryObjectStore()
DAO = InMemoryDAO()
GRAPH_VIEW = InMemoryGraphView()
EVENT_GRAPH = InMemoryEventGraph()
BM25_INDEX = InMemoryBM25Index()
VECTOR_INDEX = InMemoryVectorIndex()
GRAPH_INDEX = InMemoryGraphIndex()


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


@app.post("/documents/upload")
async def upload_document(
    authorization: str = Header(None),
    file: UploadFile = File(...),
) -> Dict[str, Any]:
    _require_api_token(authorization)
    content = await file.read()
    object_key = f"uploads/{file.filename}"
    DOCUMENT_STORE.put(object_key, content)

    memory = memory_manager.MemoryManager()
    pipeline = IngestPipeline(
        memory=memory,
        dao=DAO,
        bm25=BM25_INDEX,
        vec=VECTOR_INDEX,
        graph_idx=GRAPH_INDEX,
        graph_view=GRAPH_VIEW,
        object_store=DOCUMENT_STORE,
    )
    event = pipeline.ingest_pdf(object_key)
    return {
        "document_id": event.id,
        "object_key": object_key,
        "summary": event.attrs["text"],
    }

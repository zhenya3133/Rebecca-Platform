import uuid

from fastapi import FastAPI, Header, HTTPException, Request

from orchestrator.main_workflow import main_workflow
from platform_logger import log_event
from core_adapter import CoreConfig, RebeccaCoreAdapter


app = FastAPI()

API_TOKEN = "supersecrettoken"  # TODO: поменять на свой
CORE_CONFIG = CoreConfig.load()
CORE_ADAPTER = RebeccaCoreAdapter.from_config(CORE_CONFIG)


@app.post("/run")
async def run_pipeline(request: Request, authorization: str = Header(None)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid token")

    data = await request.json()
    input_data = data.get("input_data", "")
    trace_id = data.get("trace_id", str(uuid.uuid4()))
    log_event(f"API Call: trace_id={trace_id}, input_data={input_data}, token={authorization}")
    context_envelope = CORE_ADAPTER.fetch_context(trace_id)
    result = main_workflow(input_data)
    CORE_ADAPTER.emit_event("workflow.completed", {"trace_id": trace_id})
    log_event(f"API Result: trace_id={trace_id}, result={result.get('result', '')}")
    return {"result": result, "trace_id": trace_id, "context": context_envelope}

import uuid

from fastapi import FastAPI, Header, HTTPException, Request

from orchestrator.main_workflow import main_workflow
from platform_logger import log_event


app = FastAPI()

API_TOKEN = "supersecrettoken"  # TODO: поменять на свой


@app.post("/run")
async def run_pipeline(request: Request, authorization: str = Header(None)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=403, detail="Forbidden: Invalid token")

    data = await request.json()
    input_data = data.get("input_data", "")
    trace_id = data.get("trace_id", str(uuid.uuid4()))
    log_event(f"API Call: trace_id={trace_id}, input_data={input_data}, token={authorization}")
    result = main_workflow(input_data)
    log_event(f"API Result: trace_id={trace_id}, result={result.get('result', '')}")
    return {"result": result, "trace_id": trace_id}

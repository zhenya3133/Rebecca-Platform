from fastapi import FastAPI
from pydantic import BaseModel

from orchestrator.main_workflow import main_workflow


class RunRequest(BaseModel):
    input_data: str


app = FastAPI()


@app.post("/run")
def run_pipeline(payload: RunRequest):
    return main_workflow(payload.input_data)

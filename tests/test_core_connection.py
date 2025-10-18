"""Ensures API layer exposes core context."""

import json
from fastapi.testclient import TestClient

from api import app


def test_run_pipeline_returns_context(monkeypatch):
    client = TestClient(app)

    payload = {"input_data": "hello"}
    response = client.post(
        "/run",
        headers={"Authorization": "Bearer supersecrettoken"},
        data=json.dumps(payload),
    )
    assert response.status_code == 200
    body = response.json()
    assert "trace_id" in body
    assert "context" in body
    assert body["context"].get("metadata", {}).get("source") == "droid"

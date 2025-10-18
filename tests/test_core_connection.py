"""Ensures API layer exposes core context."""

import json
from fastapi.testclient import TestClient

from api import app, CoreSettingsPayload


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


def test_health_endpoint(monkeypatch):
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_core_settings_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("REBECCA_CORE_CONFIG", str(tmp_path / "core.yaml"))
    from importlib import reload
    import api as api_module

    reload(api_module)
    client = TestClient(api_module.app)

    headers = {"Authorization": "Bearer supersecrettoken"}

    get_response = client.get("/core-settings", headers=headers)
    assert get_response.status_code == 200
    original = get_response.json()
    assert original["core"]["endpoint"].startswith("http")

    update_payload = {
        "endpoint": "http://new-core",
        "auth_token": "secret",
        "transport": "rest",
        "timeout_seconds": 45,
        "llm_default": "creative",
        "llm_fallback": "default",
        "stt_engine": "whisper",
        "tts_engine": "edge",
        "ingest_pipeline": "auto",
    }
    put_response = client.put("/core-settings", json=update_payload, headers=headers)
    assert put_response.status_code == 200
    body = put_response.json()
    assert body["core"]["endpoint"] == "http://new-core"
    assert body["core"]["auth_token"] == "secret"

    refreshed = client.get("/core-settings", headers=headers).json()
    assert refreshed["core"]["endpoint"] == "http://new-core"


def test_document_upload(tmp_path, monkeypatch):
    monkeypatch.setenv("REBECCA_CORE_CONFIG", str(tmp_path / "core.yaml"))
    from importlib import reload
    import api as api_module

    reload(api_module)
    client = TestClient(api_module.app)
    headers = {"Authorization": "Bearer supersecrettoken"}
    file_content = b"dummy pdf"
    response = client.post(
        "/documents/upload",
        headers=headers,
        files={"file": ("test.pdf", file_content, "application/pdf")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["document_id"].startswith("pdf::")
    assert "object_key" in body

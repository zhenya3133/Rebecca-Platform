"""Core configuration loader for Rebecca integration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass
class CoreConfig:
    endpoint: str
    auth_token: str
    transport: str
    timeout_seconds: int
    llm_default: str
    llm_fallback: str
    stt_engine: str
    tts_engine: str
    ingest_pipeline: str

    @classmethod
    def load(cls, path: Path | None = None) -> "CoreConfig":
        path = path or Path("config/core.yaml")
        with path.open("r", encoding="utf-8") as file:
            raw: Dict[str, Any] = yaml.safe_load(file)
        core = raw.get("core", {})
        llm = raw.get("llm", {})
        voice = raw.get("voice", {})
        documents = raw.get("documents", {})
        return cls(
            endpoint=core.get("endpoint", "http://localhost:8000"),
            auth_token=core.get("auth_token", ""),
            transport=core.get("transport", "grpc"),
            timeout_seconds=int(core.get("timeout_seconds", 30)),
            llm_default=llm.get("default", "creative"),
            llm_fallback=llm.get("fallback", "default"),
            stt_engine=voice.get("stt", "whisper"),
            tts_engine=voice.get("tts", "edge"),
            ingest_pipeline=documents.get("ingest_pipeline", "auto"),
        )

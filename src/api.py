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
from starlette.websockets import WebSocket, WebSocketDisconnect

# Optional voice / chat dependencies
try:  # pragma: no cover - optional dependency handling
    import soundfile  # type: ignore
except Exception:  # pragma: no cover
    soundfile = None
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
CHAT_SESSIONS: Dict[str, Dict[str, Any]] = {}

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


class ChatMessage(BaseModel):
    session_id: str
    role: str = "user"
    content: str


class ChatSession(BaseModel):
    session_id: str
    messages: list[ChatMessage]
    metadata: Dict[str, Any] = {}


class VoiceRequest(BaseModel):
    session_id: str
    audio_base64: str
    format: str = "wav"


class SpeechRequest(BaseModel):
    session_id: str
    text: str


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


@app.post("/chat/session")
async def start_chat_session(authorization: str = Header(None)) -> Dict[str, Any]:
    _require_api_token(authorization)
    session_id = str(uuid.uuid4())
    CHAT_SESSIONS[session_id] = {
        "messages": [],
        "metadata": {"created_at": uuid.uuid1().hex},
    }
    return {"session_id": session_id}


@app.post("/chat/message")
async def post_chat_message(
    payload: ChatMessage,
    authorization: str = Header(None),
) -> Dict[str, Any]:
    _require_api_token(authorization)
    session = CHAT_SESSIONS.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session["messages"].append(payload.dict())
    response_text = f"Echo: {payload.content}"
    session["messages"].append(
        ChatMessage(session_id=payload.session_id, role="assistant", content=response_text).dict()
    )
    return {"response": response_text, "session_id": payload.session_id}


@app.post("/voice/stt")
async def voice_to_text(payload: VoiceRequest, authorization: str = Header(None)) -> Dict[str, Any]:
    _require_api_token(authorization)
    text = f"transcribed text from {payload.format}"
    return {"session_id": payload.session_id, "text": text}


@app.post("/voice/tts")
async def text_to_voice(payload: SpeechRequest, authorization: str = Header(None)) -> Dict[str, Any]:
    _require_api_token(authorization)
    audio_stub = payload.text[::-1]
    return {"session_id": payload.session_id, "audio_base64": audio_stub, "format": "wav"}


@app.websocket("/chat/stream/{session_id}")
async def chat_stream(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    if session_id not in CHAT_SESSIONS:
        await websocket.send_json({"error": "Session not found"})
        await websocket.close()
        return
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("content", "")
            CHAT_SESSIONS[session_id]["messages"].append(
                ChatMessage(session_id=session_id, role="user", content=message).dict()
            )
            reply = f"Streaming echo: {message}"
            await websocket.send_json({"role": "assistant", "content": reply})
    except WebSocketDisconnect:
        await websocket.close()

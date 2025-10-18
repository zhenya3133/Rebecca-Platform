# Rebecca-Platform (DROId)

Rebecca/DROId is a multi-agent automation platform covering research, architecture, implementation, testing, deployment, and operations. The freeze build runs with in-memory mocks and can be upgraded to production services via configuration.

> **Freeze snapshot (2025-10-18):** API, agents, memory, chat, voice stubs, and ingestion pipelines operate locally with `python -m pytest tests/test_core_connection.py` passing.

## Highlights
- Meta-Orchestrator coordinates specialized agents (architect, research_scout, knowledge_curator, blueprint_generator, qa_guardian, sec_ops, deployment_ops, ops_commander).
- MemoryManager provides core, episodic, semantic, procedural, vault, and security layers plus AdaptiveBlueprintTracker.
- FastAPI backend exposes REST and WebSocket chat, document upload, health, and core-settings endpoints.
- React frontend delivers configuration forms, drag-and-drop ingest, and the chat panel with voice stubs.
- RebeccaCoreAdapter bridges to the Rebecca Core with pluggable transports.

## Mock launch
1. Install Python 3.11 and Node.js >= 18 (Docker optional).
2. Start the platform using scripts in `install/`:
   - `powershell -ExecutionPolicy Bypass -File install/setup_mock.ps1`
   - `bash install/setup_mock.sh`
   - `docker compose -f docker/docker-compose.mock.yml up`
3. API: `http://localhost:8000` (Swagger: `/docs`).
4. UI dev: `cd frontend && npm install && npm run dev -- --host` -> `http://localhost:5173`.

See `install/manual.md` for detailed steps.

## Testing
- Smoke: `python -m pytest tests/test_core_connection.py`
- Full suite: `python -m pytest`
- Frontend: `npm run lint`, `npm run test`

## Project layout
- `src/` — backend, agents, memory, adapter, ingest
- `frontend/` — React application
- `config/` — YAML configuration
- `tests/` — pytest suites
- `docker/` — mock compose stack
- `install/` — setup scripts and manual

## Going production
1. Update `config/core.yaml` (endpoints, tokens, LLM/STT/TTS preferences).
2. Provide `.env` secrets and replace in-memory DAO/ObjectStore/VectorStore in `src/api.py`.
3. Wire ingest pipeline to S3, Postgres, Qdrant, or other services.
4. Prepare production docker-compose and CI/CD pipelines.

## Documentation
- `install/manual.md` — freeze guide
- `CORE_AUDIT.md` — module and agent overview
- `CHANGELOG.md` — release history
- `AGENTS.md` — agent specifications

Feedback and contributions are welcome via issues or pull requests.

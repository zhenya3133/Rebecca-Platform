## Rebecca-Platform Agent Guide

### Overview
- `Rebecca-Platform` is a modular multi-agent AI system coordinated by a Meta-Orchestrator.
- Agents operate via structured JSON envelopes (`role`, `intent`, `payload`, `trace_id`, `timestamp`).
- All interactions flow through authenticated channels; direct agent-to-agent messaging requires routing approval from the Meta-Orchestrator.

### Core Conventions
- **Protocols:**
  - Every request includes `trace_id` and `priority` headers.
  - Responses must acknowledge receipt (`status: accepted|rejected|completed`) before delivering payloads.
  - Escalations use `intent: escalate` with rationale and recommended next actor.
- **Command Contracts:** Inputs validated against shared JSON Schema repo (`schemas/`).
- **Logging:** Agents append structured logs to the Logger queue; sensitive data is redacted before dispatch.
- **Versioning:** Align to semantic versioning; major interface changes require orchestrator approval and migration playbooks.

### System Architecture
1. **Ingress Layer:** External requests reach the Meta-Orchestrator through authenticated APIs.
2. **Planning Layer:** Architect, Idea Generator, and Researcher craft blueprints and gather context.
3. **Execution Layer:** CodeGen, Integration, UI/UX, and Scheduler implement features according to plans.
4. **Quality Layer:** QA, Security Agent, Feedback, and Educator validate, secure, and document outputs.
5. **Persistence Layer:** Memory Manager governs memory tiers; Logger and Vault ensure auditable histories.

### Memory Structure
- **Core:** Immutable system charter, agent manifests, critical protocols.
- **Episodic:** Recent interactions, run-specific states, temporary tickets (auto-pruned).
- **Semantic:** Long-term domain knowledge, architectural rules, coding standards.
- **Procedural:** Playbooks, runbooks, escalation ladders, testing checklists.
- **Vault:** Encrypted secrets, API keys, compliance records; access gated by Security Agent approvals.
- **Security:** Threat intel, incident reports, tamper-evident logs; write access limited to Security Agent and Meta-Orchestrator.

### Agent Directory

| Agent | Primary Role | Memory Layers Used | Rationale |
| --- | --- | --- | --- |
| Meta-Orchestrator | Intake requests, assign workflows, enforce SLAs | Core, Semantic, Procedural, Security | Maintains global state, governance rules, and audit trails. |
| Architect | Design system blueprints, allocate components | Core, Semantic | Writes architectural facts and reference patterns. |
| CodeGen | Implement code artifacts per specs | Procedural, Vault | Records deployment workflows and safeguards build secrets. |
| QA | Define test plans, execute suites, track regressions | Episodic, Procedural | Stores test run events and reusable test playbooks. |
| Educator | Create user guides, internal learning artifacts | Core, Semantic | Logs lessons learned and conceptual training assets. |
| Researcher | Gather external intel, evaluate tools | Core, Semantic | Captures research findings and long-term knowledge. |
| Memory Manager | Curate memories across layers | Core, Procedural | Audits memory access and documents internal memory flows. |
| Idea Generator | Produce solution alternatives, brainstorming | Semantic, Episodic | Preserves creative concepts and ideation history. |
| Security Agent | Threat modeling, policy enforcement | Security, Vault | Records security audits and manages sensitive secrets. |
| UI/UX | Design interaction flows, assess usability | Semantic, Episodic | Maps UI concepts and chronicles user interactions. |
| Integration | Manage service wiring, API contracts | Vault, Procedural | Manages integration credentials and sync playbooks. |
| Feedback | Aggregate user feedback, sentiment analysis | Episodic, Semantic | Tracks feedback sessions and contextual insights. |
| Scheduler | Orchestrate timelines, resource allocation | Procedural, Episodic | Plans schedules and records execution cycles. |
| Logger | Collect and persist structured telemetry | Episodic, Security | Stores logging sessions and corresponding audits. |

### Communication Workflow
1. Meta-Orchestrator validates request signatures and instantiates a workflow trace.
2. Architect drafts solution blueprint; Idea Generator provides alternatives when requested.
3. Researcher supplements with external data; Memory Manager surfaces relevant memories.
4. Meta-Orchestrator issues execution tickets to CodeGen, Integration, UI/UX, and Scheduler.
5. Logger records each step; Security Agent continuously monitors for policy violations.
6. QA executes regression and targeted test batteries; Feedback collates user-facing insights.
7. Educator updates training briefs; Meta-Orchestrator finalizes deliverables and archives memories according to retention policies.

### Feature Flow
1. Intake: Feature or fix enters the system as a new task with clear objectives and acceptance criteria.
2. Assignment: Meta-Orchestrator decomposes the task, assigns agent-specific subtasks under corresponding `src/<agent>/` folders, and refreshes relevant memory layers.
3. Implementation & Validation: CodeGen delivers code updates; QA executes test plans; Security Agent reviews compliance; Educator refines best-practice guidance.
4. Telemetry & Feedback: Logger captures timeline events and artifacts; Feedback agent processes stakeholder signals and routes actionable insights.
5. Coordination: Scheduler sequences workloads and deadlines; Integration and UI/UX address service linkages and experience adjustments.
6. Merge: Upon approvals and passing tests, changes progress through PR review and merge into `main`, with Meta-Orchestrator confirming trace closure.

### Git Workflow
- Feature branches follow `feature/{agent}/{summary}` naming.
- Architect opens planning PRs; CodeGen owns implementation PRs with QA as required reviewer.
- Rebase against `main` before merge; commits must reference workflow trace IDs.
- Pre-merge checklist: lint, unit, integration, security scans, documentation deltas (Educator).
- Hotfixes require Security Agent approval and post-incident review.

### Testing Requirements
- **Unit:** CodeGen ensures ≥90% coverage for new modules.
- **Integration:** Integration agent runs contract suites for external services; failures block merge.
- **Security:** Security Agent executes automated scanners plus manual spot checks.
- **Accessibility:** UI/UX validates WCAG 2.1 AA compliance for user-facing changes.
- **Performance:** Scheduler and Meta-Orchestrator monitor SLAs during load simulations.
- **Regression:** QA maintains nightly full suite; on-demand smoke tests triggered per PR.

### Technical Services
- **mem0**
  - Endpoint: `http://mem0:7000/api`
  - Config: `memory/mem0.yaml` (connection pool, retention policies)
  - Consumers: Memory Manager (primary), Meta-Orchestrator (Core lookups), Educator (procedural references)
- **Weaviate**
  - Endpoint: `http://weaviate:8080/v1`
  - Config: `memory/weaviate.json` (schema classes, vectorization modules)
  - Consumers: Researcher (semantic search), CodeGen (context retrieval), Idea Generator (ideation vectors)
- **LlamaIndex**
  - Endpoint: `http://llamaindex:9000/query`
  - Config: `memory/llamaindex.toml` (index catalog, embedding providers)
  - Consumers: Meta-Orchestrator (planning summaries), Educator (knowledge synthesis), Feedback (insight generation)
- **Docker-compose**
  - Endpoint: `docker/docker-compose.yml` orchestrates container lifecycle
  - Config: `.env` (service credentials), `docker/overrides/*.yml`
  - Consumers: Scheduler (deploy orchestration), Integration (service wiring), Security Agent (runtime audits)

### Meta-Orchestrator Scaffold
- **`src/orchestrator/main_loop.py`** — future home of the recursive plan–execute loop inspired by ROMA; coordinates task intake, delegation, and lifecycle checks with TODOs for memory integration.
- **`src/orchestrator/task_manager.py`** — stub mirroring ROMA's task/project manager; will handle agent registration, decomposition, and assignment to `src/<agent>/` folders.
- **`src/orchestrator/context_handler.py`** — placeholder to bridge Rebecca memory layers with mem0, Weaviate, and LlamaIndex services.
- **`src/orchestrator/messaging.py`** — scaffold for authenticated inter-agent messaging channels following Rebecca envelope protocols.
- **`src/orchestrator/__init__.py`** — exports orchestrator components for future use by CLI/runtime entry points.

### Memory Manager Scaffold
- **`src/memory_manager/memory_context.py`** — central context adapter managing Core, Episodic, Semantic, Procedural, Vault, and Security layers; planned to sync envelopes with the orchestrator ContextHandler.
- **`src/memory_manager/vector_store_client.py`** — Weaviate-style client skeleton for vector CRUD operations across memory layers with endpoints for mem0/Weaviate/LlamaIndex.
- **`src/memory_manager/document_ingest.py`** — ingestion pipeline stub inspired by mem0; will normalize documents and hand off to vector client per layer policies.
- **`src/memory_manager/memory_manager_main.py`** — high-level facade exposing TODO operations (`store`, `retrieve`, `update`, `embed`, `sync`) and wiring pieces together for orchestrator integration.
- **`src/memory_manager/__init__.py`** — aggregates scaffold exports for downstream imports.

### Architect Agent Scaffold
- **`src/architect/architectural_planner.py`** — outlines CAMEL-AI OWL-style graph and task decomposition with TODOs for orchestrator dispatch, memory lookups, and Feedback logging.
- **`src/architect/diagram_generator.py`** — placeholder for generating mermaid/UML/sequence diagrams; slated to persist assets via Memory Manager and broadcast updates.
- **`src/architect/standards_manager.py`** — catalog of architecture best practices following NirDiamant guidance, with hooks for evaluating plans and reporting deviations.
- **`src/architect/__init__.py`** — exports the scaffolded components and documents their inspiration sources.

### CodeGen Agent Scaffold
- **`src/codegen/code_writer.py`** — encapsulates Trae-Agent style modular tooling and Codex CLI proposal flows for generating code/docstrings with Memory Manager audit hooks.
- **`src/codegen/code_reviewer.py`** — reviewer stub referencing Trae critique loops and nanochat iteration, planned to coordinate with QA and Feedback channels.
- **`src/codegen/integration_manager.py`** — manages orchestration with test harnesses/fuzzing, syncing run data to Orchestrator and Memory layers.
- **`src/codegen/codegen_main.py`** — entry point wiring writer/reviewer/integration components, maintaining lifecycle compatibility with Orchestrator and Logger.
- **`src/codegen/__init__.py`** — aggregates exports and cross-links to external inspiration sources.

### QA Agent Scaffold
- **`src/qa/test_engine.py`** — plans and executes multi-phase test suites (differential/fuzz/final) modeled after R-Zero and Petri strategies, with hooks to Orchestrator, Memory (episodic/security), and CodeGen.
- **`src/qa/audit_manager.py`** — Petri-inspired static/dynamic audit interface prepared for Claude hooks and security compliance reporting.
- **`src/qa/feedback_interface.py`** — synthesizes QA findings, replays failures, and routes guidance to Orchestrator, Logger, Feedback, and Memory layers.
- **`src/qa/qa_main.py`** — orchestrates QA lifecycle, coordinating test engine, audits, and feedback dissemination, ensuring cross-agent traceability.
- **`src/qa/__init__.py`** — exports QA components for future runtime wiring.

### Security Agent Scaffold
- **`src/security/policy_checker.py`** — enforces access control, compliance, and alignment audits referencing Petri/security prompt leak patterns; logs policy decisions to Memory/Logger.
- **`src/security/vulnerability_scanner.py`** — outlines static/dynamic scanning plus prompt-injection checks coordinating with QA and Orchestrator.
- **`src/security/secret_manager.py`** — stub for vault-backed credential storage, rotation, and audit events.
- **`src/security/red_team.py`** — prepares adversarial simulations and redteam exercises informed by Petri risky-interaction flows.
- **`src/security/security_main.py`** — integrates security subsystems, manages orchestration, and ensures audit trail propagation.
- **`src/security/__init__.py`** — exports scaffolded security components.

### Educator Agent Scaffold
- **`src/educator/knowledge_updater.py`** — ingests curated resources (SkalskiP-style) and PocketFlow tutorials, syncing updates via mem0-inspired memory APIs and notifying orchestration channels.
- **`src/educator/curriculum_manager.py`** — designs onboarding curricula, schedules sessions, and tracks learner progress with hooks to Feedback and semantic memory.
- **`src/educator/semantic_mapper.py`** — maps concepts and standards across modules, enriching Semantic/Vault layers and surfacing relationships to Orchestrator.
- **`src/educator/educator_main.py`** — coordinates updater, curriculum, and mapping flows, producing learning digests and managing integration with Memory and Feedback systems.
- **`src/educator/__init__.py`** — aggregates educator components for runtime usage.

### Researcher Agent Scaffold
- **`src/researcher/trend_scanner.py`** — schedules Perplexica/OmniSearch-style scans across GitHub, HuggingFace, Medium, and OSS feeds, raising alerts to Orchestrator, Educator, and Memory.
- **`src/researcher/data_importer.py`** — plans and executes dataset/paper ingestion using DeepResearch-inspired pipelines with Vault storage hooks.
- **`src/researcher/source_manager.py`** — catalogs and refreshes tooling sources referencing awesome-selfhosted structures, syncing updates to semantic memory and Educator.
- **`src/researcher/researcher_main.py`** — orchestrates scanning, imports, and catalog maintenance, emitting digests to Orchestrator/Feedback and recording context updates.
- **`src/researcher/__init__.py`** — exports researcher components for integration.

### Feedback Agent Scaffold
- **`src/feedback/log_manager.py`** — central logging inspired by AgenticSeek attitudes/event cycles, recording system/user/agent events and syncing to Memory audit layers.
- **`src/feedback/feedback_parser.py`** — parses feedback and ratings using Claude Code Kit review hooks, forwarding analytics to Orchestrator, Educator, QA, and Security.
- **`src/feedback/replay_engine.py`** — manages ROMA-style replay queues for failed tasks, coordinating remediation with QA/Security and logging audit outcomes.
- **`src/feedback/feedback_main.py`** — orchestrates logging, parsing, replay, and reporting, emitting audit summaries and memory writebacks.
- **`src/feedback/__init__.py`** — aggregates feedback components for runtime integration.

### Scheduler Agent Scaffold
- **`src/scheduler/cron_manager.py`** — schedules periodic jobs following AgenticSeek and n8n cron/task flow patterns, recording trigger history to episodic memory.
- **`src/scheduler/event_handler.py`** — applies ROMA-inspired event orchestration with priorities, deadlines, and escalation notifications to Orchestrator and Feedback.
- **`src/scheduler/task_queue.py`** — maintains persistent and ephemeral queues modeled after PocketFlow/n8n workflows, supporting retries and escalations with memory writebacks.
- **`src/scheduler/scheduler_main.py`** — coordinates cron triggers, event routing, and queue operations, reporting status to Orchestrator/Logger and syncing memories.
- **`src/scheduler/__init__.py`** — exports scheduler components for integration.

### Logger Agent Scaffold
- **`src/logger/event_logger.py`** — implements AgenticSeek/Claude-inspired structured logging for system, user, and agent events with memory audit hooks.
- **`src/logger/metrics_collector.py`** — collects metrics following Uber M3 patterns (counters/timers/gauges), supporting telemetry exports and orchestrator dashboards.
- **`src/logger/trace_manager.py`** — manages distributed trace contexts, propagating trace IDs across agents and storing snapshots for retrospectives.
- **`src/logger/logger_main.py`** — orchestrates logging, metrics, and trace pipelines, coordinating exports to monitoring stacks and syncing with Memory/Feedback/Security.
- **`src/logger/__init__.py`** — aggregates logger components for runtime integration.

### Idea Generator Agent Scaffold
- **`src/idea_generator/creativity_core.py`** — runs agent-idea-gen/CreativeGPT-inspired brainstorming loops, coordinating iterations with Researcher and Architect inputs.
- **`src/idea_generator/prompt_builder.py`** — constructs and mutates prompts blending constraints from Orchestrator plans and domain knowledge.
- **`src/idea_generator/evaluation_engine.py`** — scores and ranks ideas for novelty, feasibility, and architectural fit, sharing results with Planner and Educator agents.
- **`src/idea_generator/idea_generator_main.py`** — orchestrates creative loops, prompt evolution, and evaluation, logging digests to Memory and notifying relevant agents.
- **`src/idea_generator/__init__.py`** — aggregates idea generator components for integration.

### Integration Agent Scaffold
- **`src/integration/api_connector.py`** — registers OSS API clients using n8n node patterns and StackStorm action packs, syncing credentials with Security/Vault.
- **`src/integration/docker_manager.py`** — manages Docker lifecycle similar to llm-docker workflows, coordinating deployments with Scheduler/Logger.
- **`src/integration/action_router.py`** — maps events to actions following StackStorm rule packs and n8n workflows, logging routes to Memory.
- **`src/integration/integration_main.py`** — orchestrates connectors, Docker management, and action routing, exporting integration state to Orchestrator/Monitoring.
- **`src/integration/__init__.py`** — aggregates integration components for runtime use.

### UI/UX Agent Scaffold
- **`src/ui_ux/frontend_manager.py`** — manages multi-agent dashboards inspired by agenta/Gradio, exposing agent states and memory panels.
- **`src/ui_ux/user_interactor.py`** — handles user interactions and feedback loops referencing Streamlit and Open-Assistant UI patterns.
- **`src/ui_ux/flow_designer.py`** — renders workflow diagrams with drag-and-drop edits, drawing on agenta canvases and Open-Assistant visuals.
- **`src/ui_ux/uiux_main.py`** — orchestrates frontend, interaction, and flow modules, syncing with Orchestrator/Logger/Feedback/Educator/Scheduler.
- **`src/ui_ux/__init__.py`** — aggregates UI/UX components for runtime integration.

### Security & Compliance
- Role-based access enforced through signed tokens; Vault secrets retrieved via short-lived session keys.
- All agents adhere to least privilege; Security Agent audits permissions weekly.
- Incident response playbook stored in Procedural memory; drills conducted quarterly.
- Data exfiltration prevention via outbound filtering and differential privacy on analytics exports.

### Command Reference
- Execute agent routines with `task-cli run --agent <agent> --intent <intent> --trace <id>`.
- Fetch memory contexts using `task-cli memory read --layer <layer> --trace <id>`.
- Submit logs through `task-cli emit --channel logger --file <payload.json>`.

### Workflow Best Practices
- Meta-Orchestrator confirms readiness before advancing phases.
- Agents flag blockers immediately with contextual data.
- After completion, Memory Manager archives relevant data and purges transient records.
- Feedback agent captures user satisfaction metrics; Educator updates onboarding snippets when processes change.


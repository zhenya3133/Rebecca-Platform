# Rebecca-Platform

Rebecca-Platform — это координируемая мультиагентная AI-система для проектирования, реализации, тестирования и деплоя фичей с минимальным ручным вмешательством.

> **Current status:** ядро собранo и проверено на in-memory адаптерах, тесты зелёные (`python -m pytest src/tests`), платформа готова к подключению production-хранилищ и LLM.

## Как устроен пайплайн

- Каждый агент взаимодействует через контролирующий Meta-Orchestrator.
- Задачи декомпозируются и распределяются по агентам в папке `src/<agent>`.
- Память (MemoryManager) реализует 6 слоёв: Core, Episodic, Semantic, Procedural, Vault, Security.
- Данные между агентами передаются через структурированные JSON-конверты с метаданными (`role`, `intent`, `payload`, `trace_id`).
- Логирование и обработка ошибок осуществляется через модуль `platform_logger` (ранее `logger`).

## Что такое слои памяти

- **Core:** системные правила, манифесты агентов.
- **Episodic:** свежие события, временные записи (автоматически чистятся).
- **Semantic:** long-term знания, стандарты, рекомендации.
- **Procedural:** инструкции, чеклисты, runbook-и.
- **Vault:** секреты и токены, хранилище для приватных данных.
- **Security:** аудиты, отчёты, логи инцидентов (только для Security Agent и Meta-Orchestrator).

## Как запускать тесты

### Локальные smoke-тесты агентов
1. Перейти в папку агента:
   ```
   cd src/<agent>
   ```
2. Запустить smoke-тест:
   ```
   python test_main.py
   ```
3. Проверить вывод: ОК означает, что агент корректно взаимодействует с памятью и логирует свои действия.

### Интеграционные проверки retrieval/ingest
```
python -m pytest tests/retrieval/test_new_cases.py
```
Тест `test_edge_cases` валидирует гибридный ретривер на шумных запросах, а `test_pdf_ingest` убеждается, что пайплайн PDF фиксирует артефакты в семантической памяти.

## Начало работы

1. Клонируй репозиторий:
   ```
   git clone <repo-url>
   cd Rebecca-Platform
   ```
2. Запусти базовые сервисы (docker, если требуется):
   ```
   docker compose -f docker/docker-compose.yml up -d
   ```
3. Проведи тестирование и взаимодействие с агентами через CLI:
   ```
   task-cli run --agent <agent> --intent <intent> --trace <id>
   task-cli test --suite smoke
   ```

## CI/CD
- Все pull-request и коммиты автоматически тестируются (GitHub Actions: .github/workflows/tests.yml).
- Проверяются smoke-тесты для каждого агента и интеграционный тест.
- При ошибке сборка блокируется, требуется исправление.

### Observability & Regression Metrics
- Для retrieval-модулей собираются метрики `coverage@k`, `contradiction-rate`, `token-efficiency`, `drift_score`, `privacy_violation_rate`.
- Цель качества на golden set — менее 1% ошибок по каждой из этих метрик; `drift_score` должен быть < 0.1, нарушений политики — 0.
- Nightly задача `tests/nightly_eval.py` запускает регрессионный контроль и выводит значения метрик.

## Внешний API

- Стартап:
  ```
  pip install -r src/requirements.txt
  cd src
  uvicorn api:app --reload
  ```
- Доступно в браузере: http://localhost:8000/docs (Swagger UI)
- Пример вызова через curl:
  ```
  curl -X POST "http://localhost:8000/run" -H "accept: application/json" -H "Content-Type: application/json" -d "\"test input\""
  ```

## Запуск API с авторизацией и trace_id

1. Старт сервера:
   ```
   uvicorn api:app --reload
   ```
2. Запрос:
   ```
   curl -X POST "http://localhost:8000/run" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer supersecrettoken" \
     -d "{\"input_data\": \"Ваш input\", \"trace_id\": \"unique-id-123\"}"
   ```
3. В логах (`agent_log.txt`) записывается `trace_id` и результаты для каждого запроса.

---

**Вопросы/исправления — см. документацию AGENTS.md или обращайся к Meta-Orchestrator.**

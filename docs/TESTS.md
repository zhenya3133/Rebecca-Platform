# Rebecca-Platform Test Guide

## Overview

Тестовый набор состоит из smoke-проверок для агентов, nightly регрессионных сценариев и интеграций retrieval/ingest.

## Smoke-тесты агентов
- Расположены в `src/<agent>/test_main.py`.
- Запуск: `python src/<agent>/test_main.py` — проверяет доступ к слоям памяти и базовую оркестрацию.

## Интеграционные тесты Retrieval/Ingest
- Файл: `tests/retrieval/test_new_cases.py`.
- Проверяет:
  - `test_edge_cases`: устойчивость гибридного ретривера к шумным и мультиязычным запросам.
  - `test_pdf_ingest`: фиксацию ingest-пайплайна PDF в семантической памяти.
- Запуск: `python -m pytest tests/retrieval/test_new_cases.py`.

## Nightly Regression Suite
- Файл: `tests/nightly_eval.py`.
- Собирает метрики coverage, contradiction rate, token efficiency, drift score и privacy violation rate.
- Рекомендуемый запуск в CRON/CI: `python -m pytest tests/nightly_eval.py`.

## CI Pipeline
- GitHub Actions workflow: `.github/workflows/tests.yml`.
- Выполняет smoke-тесты агентов, интеграционные проверки и nightly-метрики перед merge.

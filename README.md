# AI Service Demo (FastAPI, LangChain, Celery, Guardrails)

This is a **complete, educational demo repo** designed to mirror what a strong
Senior AI Engineer / Backend Engineer would build for **document intelligence + RAG**
in a production-ish environment.

It focuses on:

- Clean **FastAPI** microservice architecture (routers, schemas, services, DI).
- **RAG-style pipeline** (chunk → vector store → retrieve → LLM) using a simple
  vector store and a pluggable LangChain/Azure client.
- **Guardrails and validation**:
  - Pydantic schema enforcement
  - Semantic validation (e.g. numeric constraints)
  - Simple PII detector
  - "Grounded answer" mode to reduce hallucinations.
- **Async-ready design** and clear seams where async I/O would go.
- **Celery task queue** for long-running background jobs (RabbitMQ/Redis broker).
- **Metrics collection** (latency, failures) and a `/metrics` endpoint.
- **Dependency Injection** everywhere via FastAPI `Depends()`.

> NOTE: This project is **offline-friendly** by default.
> The LLM is implemented as a `FakeLLM` that behaves deterministically so you
> can run and understand everything without API keys.
> To connect to Azure OpenAI, you only need to implement the TODO in
> `app/services/llm_client.py`.

## Quickstart

### 1. Create venv and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Run the API (without Celery/queues)

```bash
uvicorn app.main:app --reload
```

Open docs at: http://127.0.0.1:8000/docs

Test payload:

```json
{
  "query": "invoice total and currency",
  "fields": ["invoice_no", "total_amount", "currency", "date"]
}
```

POST to `/api/extract`.

### 3. Enable Celery (optional, if you have a broker like Redis or RabbitMQ)

Start the worker **in another terminal**:

```bash
celery -A app.workers.celery_app.celery worker --loglevel=info
```

Then use `/api/extract/async` which enqueues a background task.

You can inspect task status via `/api/extract/status/{task_id}` (toy implementation).

## Project Layout

```text
app/
  main.py               # FastAPI app + lifespan
  core/
    config.py           # Settings via pydantic-settings
    logging.py          # Basic logging config
    security.py         # Placeholder auth (JWT hook point)
  api/
    deps.py             # Dependency-injection wiring
    routers/
      health.py         # /health
      extract.py        # /api/extract, /api/extract/async, /status
      metrics.py        # /metrics
  models/
    db_models.py        # SQLModel example (not heavily used)
  schemas/
    extract.py          # Request/response schemas
  services/
    chunker.py          # Document chunking
    vectorstore.py      # Simple in-memory vector store (cosine similarity)
    llm_client.py       # FakeLLM + AzureLangChainLLM interface
    validation.py       # Pydantic schema + semantic + PII checks
    metrics.py          # MetricsCollector
    pipeline.py         # RAG + extraction pipeline orchestration
  workers/
    celery_app.py       # Celery init + tasks
  tests/
    test_extract.py     # Example unit test
data/
  sample_invoice.txt    # Sample document for indexing
```

This repo is meant as a **teaching + interview-prep tool**:
you can walk through each file and understand how a senior engineer would
structure a realistic AI microservice with strong software engineering practices.
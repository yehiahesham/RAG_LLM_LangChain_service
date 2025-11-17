from celery import Celery
from app.core.config import settings
from app.services.validation import ExtractionValidator
from app.services.chunker import Chunker
from app.services.vectorstore import SimpleVectorStore
from app.services.llm_client import FakeLLM
from app.services.pipeline import ExtractionPipeline
from app.services.metrics import MetricsCollector

celery = Celery(
    "ai_service_demo",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

chunker = Chunker(chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP)
vector_store = SimpleVectorStore()
with open("data/sample_invoice.txt", "r", encoding="utf-8") as f:
    docs = chunker.split(f.read())
vector_store.build_index(docs)

validator = ExtractionValidator()
metrics = MetricsCollector()
llm = FakeLLM(temperature=settings.TEMPERATURE)


@celery.task
def run_extraction_task(payload: dict):
    pipeline = ExtractionPipeline(
        vector_store=vector_store,
        llm=llm,
        validator=validator,
        metrics=metrics,
        top_k=settings.TOP_K,
        sim_threshold=settings.SIM_THRESHOLD,
    )
    import asyncio
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(pipeline.run(
        query=payload["query"],
        fields=payload["fields"],
        max_retries=settings.MAX_RETRIES,
    ))
    return result
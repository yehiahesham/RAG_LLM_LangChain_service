from fastapi import Depends
from app.core.config import settings
from app.core.security import get_current_user
from app.services.chunker import Chunker
from app.services.vectorstore import SimpleVectorStore
from app.services.llm_client import FakeLLM, RetryPolicy, LLMClient
from app.services.validation import ExtractionValidator
from app.services.metrics import MetricsCollector
from app.services.pipeline import ExtractionPipeline

chunker = Chunker(chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP)
vector_store = SimpleVectorStore()
metrics = MetricsCollector()
validator = ExtractionValidator()

with open("data/sample_invoice.txt", "r", encoding="utf-8") as f:
    docs = chunker.split(f.read())
vector_store.build_index(docs)


def get_settings():
    return settings


def get_metrics() -> MetricsCollector:
    return metrics


def get_current_user_dep():
    return get_current_user()


def get_vector_store() -> SimpleVectorStore:
    return vector_store


def get_chunker() -> Chunker:
    return chunker


def get_llm() -> LLMClient:
    return FakeLLM(temperature=settings.TEMPERATURE)


def get_retry_policy() -> RetryPolicy:
    return RetryPolicy(max_retries=settings.MAX_RETRIES)


def get_validator() -> ExtractionValidator:
    return validator


def get_pipeline(
    store: SimpleVectorStore = Depends(get_vector_store),
    llm: LLMClient = Depends(get_llm),
    validator: ExtractionValidator = Depends(get_validator),
    metrics: MetricsCollector = Depends(get_metrics),
    cfg=Depends(get_settings),
) -> ExtractionPipeline:
    return ExtractionPipeline(
        vector_store=store,
        llm=llm,
        validator=validator,
        metrics=metrics,
        top_k=cfg.TOP_K,
        sim_threshold=cfg.SIM_THRESHOLD,
    )
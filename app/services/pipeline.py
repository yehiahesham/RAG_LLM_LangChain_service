from typing import List
from app.services.vectorstore import SimpleVectorStore
from app.services.llm_client import LLMClient
from app.services.validation import ExtractionValidator
from app.services.metrics import MetricsCollector, Timed


class ExtractionPipeline:
    def __init__(
        self,
        vector_store: SimpleVectorStore,
        llm: LLMClient,
        validator: ExtractionValidator,
        metrics: MetricsCollector,
        top_k: int = 5,
        sim_threshold: float = 0.1,
    ):
        self.vector_store = vector_store
        self.llm = llm
        self.validator = validator
        self.metrics = metrics
        self.top_k = top_k
        self.sim_threshold = sim_threshold

    async def run(self, query: str, fields: List[str], max_retries: int) -> dict:
        with Timed() as t:
            context_docs = self._retrieve_context(query)
            if not context_docs:
                self.metrics.record_request(latency=0.0, success=False)
                raise ValueError("No relevant context found; cannot answer without hallucinating.")

            context = "\n\n".join(context_docs)
            attempts = 0
            last_err = None

            while attempts <= max_retries:
                attempts += 1
                strict_suffix = "" if attempts == 1 else " IMPORTANT: VALID JSON ONLY. MATCH FIELD NAMES EXACTLY. NO EXTRA KEYS."
                self.llm.temperature = 0.0

                sys_prompt = (
                    "You are an extraction engine. Extract the requested fields as strict JSON. "
                    "If information is not present in the context, use null. Do NOT guess. "
                    "Only use the provided context. If context doesn't contain the answer, use null."
                )

                raw = await self.llm.generate(sys_prompt + strict_suffix, fields=fields, context=context)
                try:
                    payload = self.validator.parse_and_validate(raw)
                    self.metrics.record_request(latency=t.elapsed, success=True)
                    grounded = True
                    return {
                        "data": payload,
                        "attempts": attempts,
                        "grounded": grounded,
                        "notes": None if attempts == 1 else f"Validated after {attempts} attempts.",
                    }
                except Exception as e:
                    last_err = str(e)
                    if attempts > max_retries:
                        self.metrics.record_request(latency=t.elapsed, success=False)
                        raise ValueError(f"Validation failed after {attempts} attempts: {last_err}")

    def _retrieve_context(self, query: str) -> List[str]:
        hits = self.vector_store.similarity_search(query, k=self.top_k)
        return [doc for doc, score in hits if score >= self.sim_threshold]
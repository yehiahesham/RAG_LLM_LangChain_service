import json
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RetryPolicy:
    max_retries: int = 2


class LLMClient:
    temperature: float = 0.0

    async def generate(self, sys_prompt: str, fields: List[str], context: str) -> str:
        raise NotImplementedError


class FakeLLM(LLMClient):
    def __init__(self, temperature: float = 0.0):
        self.temperature = temperature

    async def generate(self, sys_prompt: str, fields: List[str], context: str) -> str:
        data: Dict[str, Any] = {}
        lower = context.lower()
        for f in fields:
            key = f.strip()
            if key in ("invoice_no", "invoice id", "invoiceid"):
                data["invoice_no"] = "INV-001" if "inv-001" in lower or "invoice number" in lower else None
            elif key in ("total_amount", "total"):
                data["total_amount"] = 123.45 if "123.45" in lower or "total" in lower else None
            elif key == "currency":
                data["currency"] = "EUR" if "eur" in lower else None
            elif key == "date":
                data["date"] = "2024-05-12" if "2024-05-12" in lower else None
            else:
                data[key] = None

        if self.temperature > 0.1 and "IMPORTANT" not in sys_prompt:
            data["extra_field"] = "should_trigger_retry"

        return json.dumps(data)
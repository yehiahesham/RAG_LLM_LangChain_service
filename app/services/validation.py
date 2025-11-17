import json
import re
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError


class ExtractionSchema(BaseModel):
    invoice_no: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    date: Optional[str] = Field(None, pattern=r"\d{4}-\d{2}-\d{2}")


class ExtractionValidator:
    def parse_and_validate(self, raw: str) -> Dict[str, Any]:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from model: {e}")

        try:
            obj = ExtractionSchema(**data)
        except ValidationError as e:
            raise ValueError(f"Schema validation error: {e}")

        payload = obj.model_dump()

        if payload.get("total_amount") is not None and payload["total_amount"] <= 0:
            raise ValueError("total_amount must be > 0")

        if payload.get("currency") is not None and payload["currency"] not in ("EUR", "USD", "GBP"):
            raise ValueError("Unsupported currency; expected EUR, USD, or GBP")

        if payload.get("date") is not None and not re.match(r"\d{4}-\d{2}-\d{2}", payload["date"]):
            raise ValueError("Invalid date format, expected YYYY-MM-DD")

        if self.contains_pii(" ".join(str(v) for v in payload.values() if v is not None)):
            raise ValueError("PII detected in output; refusing result")

        return payload

    @staticmethod
    def contains_pii(text: str) -> bool:
        ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"
        return bool(re.search(ssn_pattern, text))
from pydantic import BaseModel, Field
from typing import List, Optional, Any


class ExtractRequest(BaseModel):
    query: str = Field(..., min_length=2)
    fields: List[str] = Field(..., min_items=1, max_items=20)


class ExtractResult(BaseModel):
    data: dict
    attempts: int
    grounded: bool
    notes: Optional[str] = None


class AsyncTaskResponse(BaseModel):
    task_id: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None
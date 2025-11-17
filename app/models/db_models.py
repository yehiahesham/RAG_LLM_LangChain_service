from sqlmodel import SQLModel, Field
from typing import Optional


class ExtractionJob(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    query: str
    status: str = "pending"
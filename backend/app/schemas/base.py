from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    key: str = Field(pattern=r"[A-Z]+-\d+")
    created: datetime
    updated: datetime
    summary: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
from datetime import datetime
from typing import Optional, List
from pydantic import Field
from .base import BaseSchema

class TaskSchema(BaseSchema):
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    epic_key: Optional[str] = Field(None, pattern=r"[A-Z]+-\d+")
    labels: List[str] = []
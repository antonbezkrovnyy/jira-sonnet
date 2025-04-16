from typing import List
from pydantic import Field
from .base import BaseSchema

class EpicSchema(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    tasks: List[str] = []  # Changed from Field(default_list=[]) to direct default
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LabelSchema(BaseModel):
    """Schema for JIRA label"""
    key: str = Field(..., description="Label key (usually lowercase)")
    name: str = Field(..., description="Label display name")
    description: Optional[str] = Field(None, description="Optional label description")
    color: Optional[str] = Field(None, pattern="^#[0-9a-fA-F]{6}$", description="Color in hex format")
    created: datetime
    updated: datetime
    used_in: List[str] = Field(default_factory=list, description="List of issue keys using this label")
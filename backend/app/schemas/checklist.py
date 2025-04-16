from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ChecklistType(str, Enum):
    """Type of checklist"""
    DOR = "dor"
    DOD = "dod"

class ChecklistSchema(BaseModel):
    """Schema for DoR/DoD checklists"""
    key: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Display name")
    type: ChecklistType = Field(..., description="Type of checklist (DoR/DoD)")
    text: str = Field(..., description="Checklist content")
    created: datetime
    updated: datetime

class ChecklistTemplate(BaseModel):
    """Template metadata from markdown file"""
    key: str = Field(..., description="Template file name without extension")
    name: str = Field(..., description="Display name from frontmatter")
    description: str = Field(..., description="Template description")
    version: str = Field(..., description="Template version")
    type: ChecklistType
    content: str = Field(..., description="Markdown content without frontmatter")
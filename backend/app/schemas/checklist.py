from pydantic import BaseModel, Field
from enum import Enum

class ChecklistType(str, Enum):
    """Type of checklist"""
    DOR = "dor"
    DOD = "dod"

class ChecklistTemplate(BaseModel):
    """Schema for DoR/DoD checklists"""
    key: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Display name")
    type: ChecklistType = Field(..., description="Type of checklist (DoR/DoD)")
    description: str = Field(..., description="Template description")
    version: str = Field(..., description="Template version")
    content: str = Field(..., description="Checklist content")
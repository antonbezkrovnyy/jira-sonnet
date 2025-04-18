from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TaskPriority(str, Enum):
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOWEST = "Lowest"

class CreateTaskRequest(BaseModel):
    # Required fields
    project_key: str = Field(..., description="Project key")
    summary: str = Field(..., min_length=1, max_length=255)
    
    # Main fields
    description: Optional[str] = None
    issue_type: str = Field(default="Engineer")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    
    # Time fields
    due_date: Optional[datetime] = None
    estimate: Optional[float] = Field(None, ge=0)
    
    # Relations
    epic_link: Optional[str] = None
    
    # Labels and assignee
    labels: Optional[List[str]] = Field(default_factory=list)
    assignee: Optional[str] = None
    reporter: Optional[str] = None  # Add reporter field

    class Config:
        json_schema_extra = {
            "example": {
                "project_key": "PROJ",
                "summary": "Implement new feature",
                "description": "Detailed description...",
                "issue_type": "Engineer", 
                "priority": "Medium",
                "due_date": "2024-12-31T23:59:59Z",
                "estimate": 8.0,
                "epic_link": "PROJ-123",
                "labels": ["backend", "feature"],
                "assignee": "john.doe",
                "custom_fields": {
                    "story_points": 5,
                    "team": "backend"
                }
            }
        }
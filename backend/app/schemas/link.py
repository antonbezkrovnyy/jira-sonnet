from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class LinkType(str, Enum):
    """Internal JIRA link types"""
    BLOCKS = "blocks"
    BLOCKED_BY = "is blocked by"
    RELATES_TO = "relates to"
    DUPLICATES = "duplicates"
    DUPLICATED_BY = "is duplicated by"

class ResourceType(str, Enum):
    """External resource types"""
    CONFLUENCE = "confluence"
    WEB = "web"
    GDOC = "gdoc"

class BaseLink(BaseModel):
    """Base link model"""
    id: str = Field(..., description="Link identifier")
    source: str = Field(..., description="Source task key")
    created: Optional[datetime] = Field(None, description="Link creation date if available")
    updated: Optional[datetime] = Field(None, description="Link last update date")

class TaskLink(BaseLink):
    """Internal task link model"""
    type: LinkType = Field(..., description="Link type")
    target: str = Field(..., description="Target task key")

class ExternalLink(BaseLink):
    """External resource link model"""
    type: ResourceType = Field(..., description="Resource type")
    target: str = Field(..., description="Resource identifier")
    title: str = Field(..., description="Link title")
    url: HttpUrl = Field(..., description="Resource URL")

class CreateTaskLinkRequest(BaseModel):
    """Request body for creating task link"""
    type: LinkType = Field(..., description="Link type")
    target: str = Field(..., description="Target task key")

class CreateExternalLinkRequest(BaseModel):
    """Request body for creating external link"""
    type: ResourceType = Field(..., description="Resource type")
    target: str = Field(..., description="Resource identifier")
    title: str = Field(..., description="Link title")
    url: HttpUrl = Field(..., description="Resource URL")
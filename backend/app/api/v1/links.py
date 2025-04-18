from fastapi import APIRouter, HTTPException, Depends
from app.services.links import LinksService
from app.services.external_links import ExternalLinksService
from app.schemas.link import (
    TaskLink,
    ExternalLink,
    CreateTaskLinkRequest,
    CreateExternalLinkRequest
)
from typing import List

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["links"]
)

def get_links_service():
    return LinksService()

def get_external_links_service():
    return ExternalLinksService()

@router.get("/{task_key}/links", response_model=List[TaskLink])
async def get_task_links(
    task_key: str,
    links_service: LinksService = Depends(get_links_service)
):
    """Get all links for a task"""
    return links_service.get_task_links(task_key)

@router.post("/{task_key}/links", response_model=TaskLink)
async def create_task_link(
    task_key: str,
    link: CreateTaskLinkRequest,
    links_service: LinksService = Depends(get_links_service)
):
    """Create new task link"""
    created_link = links_service.create_task_link(
        source=task_key,
        link_type=link.type,
        target=link.target
    )
    if not created_link:
        raise HTTPException(status_code=400, detail="Failed to create link")
    return created_link

@router.get("/{task_key}/external-links", response_model=List[ExternalLink])
async def get_external_links(
    task_key: str,
    external_links_service: ExternalLinksService = Depends(get_external_links_service)
):
    """Get all external links for a task"""
    return external_links_service.get_external_links(task_key)

@router.post("/{task_key}/external-links", response_model=ExternalLink)
async def create_external_link(
    task_key: str,
    link: CreateExternalLinkRequest,
    external_links_service: ExternalLinksService = Depends(get_external_links_service)
):
    """Create new external link"""
    created_link = external_links_service.create_external_link(
        task_key=task_key,
        title=link.title,
        url=link.url,
        link_type=link.type
    )
    if not created_link:
        raise HTTPException(status_code=400, detail="Failed to create external link")
    return created_link
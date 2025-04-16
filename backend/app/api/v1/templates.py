from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel, Field
from app.schemas.checklist import ChecklistTemplate, ChecklistType
from app.services.templates import get_template_service
from app.core.logging import get_logger, log_request_response

router = APIRouter(prefix="/api/v1/templates", tags=["templates"])
logger = get_logger()

class UpdateTemplateRequest(BaseModel):
    """Request body for template update"""
    name: str = Field(..., description="Template display name")
    description: str = Field(..., description="Template description")
    content: str = Field(..., description="Template markdown content")
    version: str = Field(default="1.0", description="Template version")

@router.get("/{type}")
async def list_templates(type: ChecklistType) -> List[ChecklistTemplate]:
    """Get all templates of specified type"""
    try:
        service = get_template_service()
        templates = service.get_templates(type)
        if not templates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No {type.value} templates found"  # Use type.value instead of type
            )
        return templates
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list templates"
        )

@router.get(
    "/{type}/{key}",
    response_model=ChecklistTemplate,
    responses={
        404: {"description": "Template not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_template(type: ChecklistType, key: str) -> ChecklistTemplate:
    """Get specific template by type and key"""
    try:
        service = get_template_service()
        template = service.get_template(type, key)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {key} not found"
            )
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get template"
        )

@router.put(
    "/{type}/{key}",
    response_model=ChecklistTemplate,
    responses={
        404: {"description": "Template not found"},
        500: {"description": "Internal server error"}
    }
)
async def update_template(
    type: ChecklistType,
    key: str,
    template: UpdateTemplateRequest
) -> ChecklistTemplate:
    """Update existing template"""
    try:
        service = get_template_service()
        updated = service.update_template(
            type=type,
            key=key,
            name=template.name,
            description=template.description,
            content=template.content,
            version=template.version
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {key} not found"
            )
        return updated
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update template"
        )

@router.delete(
    "/{type}/{key}",
    response_model=bool,
    responses={
        404: {"description": "Template not found"},
        500: {"description": "Internal server error"}
    }
)
async def delete_template(type: ChecklistType, key: str) -> bool:
    """Delete template"""
    try:
        service = get_template_service()
        if not service.delete_template(type, key):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {key} not found"
            )
        return True
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete template"
        )
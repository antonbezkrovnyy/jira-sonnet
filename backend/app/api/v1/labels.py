from fastapi import APIRouter, HTTPException, status, Request
from typing import List
from app.schemas.label import LabelSchema
from app.services.labels import get_label, get_project_labels
from app.core.logging import get_logger, log_request_response

router = APIRouter(prefix="/api/v1/labels", tags=["labels"])
logger = get_logger()

@router.get(
    "/{key}",
    response_model=LabelSchema,
    responses={
        404: {"description": "Label not found"},
        500: {"description": "JIRA API error"}
    }
)
async def read_label(request: Request, key: str) -> LabelSchema:
    """Get label by key"""
    logger.info(f"API request: GET label {key}")
    try:
        label = await get_label(key)
        
        if label is None:
            error_msg = f"Label {key} not found"
            log_request_response(
                logger=logger,
                endpoint=str(request.url),
                request_data={"key": key},
                error=Exception(error_msg)
            )
            raise HTTPException(status_code=404, detail=error_msg)
            
        log_request_response(
            logger=logger,
            endpoint=str(request.url),
            request_data={"key": key},
            response_data=label.model_dump()
        )
        return label
    except HTTPException:
        raise
    except Exception as e:
        log_request_response(
            logger=logger,
            endpoint=str(request.url),
            request_data={"key": key},
            error=e
        )
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/",
    response_model=List[LabelSchema],
    responses={
        500: {"description": "JIRA API error"}
    }
)
async def list_labels(request: Request) -> List[LabelSchema]:
    """Get all project labels"""
    logger.info("API request: GET labels list")
    try:
        labels = await get_project_labels()
        log_request_response(
            logger=logger,
            endpoint=str(request.url),
            response_data=[l.model_dump() for l in labels]
        )
        return labels
    except Exception as e:
        log_request_response(
            logger=logger,
            endpoint=str(request.url),
            error=e
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
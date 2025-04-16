from fastapi import APIRouter, HTTPException, status
from typing import Dict, Optional
from app.schemas.task import TaskSchema
from app.services.jira import get_task
from app.core.logging import get_logger

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
logger = get_logger()

@router.get(
    "/{key}",
    response_model=TaskSchema,
    responses={
        404: {"description": "Task not found"},
        401: {"description": "JIRA authentication failed"},
        500: {"description": "JIRA API error"}
    }
)
async def read_task(key: str) -> TaskSchema:
    try:
        logger.info(f"Fetching task with key {key}")
        task = await get_task(key)
        
        if task is None:
            logger.warning(f"Task {key} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {key} not found"
            )
        logger.info(f"Successfully retrieved task {key}")
        return task
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Invalid task request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to fetch task {key}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch task from JIRA"
        )
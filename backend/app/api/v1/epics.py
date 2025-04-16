from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.task import TaskSchema
from app.schemas.epic import EpicSchema
from app.services.jira import get_epic, get_epic_tasks
from app.core.logging import get_logger

router = APIRouter(prefix="/api/v1/epics", tags=["epics"])
logger = get_logger()

@router.get(
    "/{key}",
    response_model=EpicSchema,
    responses={
        404: {"description": "Epic not found"},
        401: {"description": "JIRA authentication failed"},
        500: {"description": "JIRA API error"}
    }
)
async def read_epic(key: str) -> EpicSchema:
    try:
        logger.info(f"Fetching epic with key {key}")
        epic = await get_epic(key)
        
        if epic is None:
            logger.warning(f"Epic {key} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Epic {key} not found"
            )
        logger.info(f"Successfully retrieved epic {key}")
        return epic
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch epic {key}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch epic from JIRA"
        )

@router.get(
    "/{key}/tasks",
    response_model=List[TaskSchema],
    responses={
        404: {"description": "Epic not found"},
        401: {"description": "JIRA authentication failed"},
        500: {"description": "JIRA API error"}
    }
)
async def read_epic_tasks(key: str) -> List[TaskSchema]:
    try:
        logger.info(f"Fetching tasks for epic {key}")
        tasks = await get_epic_tasks(key)
        
        if tasks is None:
            logger.warning(f"Epic {key} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Epic {key} not found"
            )
        logger.info(f"Successfully retrieved tasks for epic {key}")
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch tasks for epic {key}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch epic tasks from JIRA"
        )
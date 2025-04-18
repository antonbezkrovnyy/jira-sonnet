from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Optional, List
from app.schemas.task import TaskSchema
from app.schemas.create_task import CreateTaskRequest
from app.services.jira import get_task
from app.services.tasks import TasksService
from app.core.logging import get_logger

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
logger = get_logger()

def get_tasks_service():
    return TasksService()

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

@router.post("/", response_model=dict)
async def create_task(
    request: CreateTaskRequest,
    tasks_service: TasksService = Depends(get_tasks_service)
):
    """
    Create new JIRA task
    
    Returns:
        dict: Created task data including key and id
    """
    result = tasks_service.create_task(request)
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Failed to create task"
        )
    return result

@router.get("/types/{project_key}", response_model=List[dict])
async def get_task_types(
    project_key: str,
    tasks_service: TasksService = Depends(get_tasks_service)
):
    """
    Get available task types for project
    
    Args:
        project_key: JIRA project key
        
    Returns:
        List[dict]: List of available issue types with id and name
    """
    types = tasks_service.get_task_types(project_key)
    if not types:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_key} not found or no task types available"
        )
    return types
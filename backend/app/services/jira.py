from functools import lru_cache
from typing import List, Optional
from jira import JIRA
from app.core.config import get_settings
from app.schemas.task import TaskSchema
from app.schemas.epic import EpicSchema

@lru_cache()
def get_jira_client() -> JIRA:
    settings = get_settings()
    return JIRA(
        server=settings['jira_url'],
        basic_auth=(settings['jira_user'], settings['jira_token'])
    )

async def get_task(key: str) -> Optional[TaskSchema]:
    try:
        client = get_jira_client()
        issue = client.issue(key)
        return TaskSchema(
            key=issue.key,
            summary=issue.fields.summary,
            description=issue.fields.description,
            created=issue.fields.created,
            updated=issue.fields.updated
        )
    except Exception as e:
        return None

async def get_epic(key: str) -> Optional[EpicSchema]:
    try:
        client = get_jira_client()
        epic = client.issue(key)
        
        # Get epic name from customfield_10604
        epic_name = getattr(epic.fields, 'customfield_10604', None)
        
        # Get linked tasks using Epic Link field with epic key
        tasks = client.search_issues(
            f'"Epic Link" = {key} AND issuetype = Engineer',
            maxResults=50
        )
        task_keys = [task.key for task in tasks]
        
        return EpicSchema(
            key=epic.key,
            name=epic_name,
            summary=epic.fields.summary,
            description=epic.fields.description,
            created=epic.fields.created,
            updated=epic.fields.updated,
            tasks=task_keys
        )
    except Exception as e:
        print(f"Error in get_epic: {str(e)}")
        return None

async def get_epic_tasks(key: str) -> Optional[List[TaskSchema]]:
    try:
        client = get_jira_client()
        
        # Search tasks using Epic Link field with epic key
        tasks = client.search_issues(
            f'"Epic Link" = {key} AND issuetype = Engineer',
            maxResults=50
        )
        return [
            TaskSchema(
                key=task.key,
                summary=task.fields.summary,
                description=task.fields.description,
                created=task.fields.created,
                updated=task.fields.updated
            ) 
            for task in tasks
        ]
    except Exception as e:
        print(f"Error in get_epic_tasks: {str(e)}")
        return None
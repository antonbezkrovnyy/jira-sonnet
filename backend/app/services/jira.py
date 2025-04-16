from functools import lru_cache
from typing import Optional
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
        tasks = [link.outwardIssue.key 
                for link in epic.fields.issuelinks 
                if hasattr(link, 'outwardIssue')]
        return EpicSchema(
            key=epic.key,
            name=epic.fields.customfield_10014,
            summary=epic.fields.summary,
            description=epic.fields.description,
            created=epic.fields.created,
            updated=epic.fields.updated,
            tasks=tasks
        )
    except Exception as e:
        return None
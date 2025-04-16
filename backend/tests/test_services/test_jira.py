from datetime import datetime
import pytest
from unittest.mock import Mock, patch
from app.services.jira import get_task, get_epic

@pytest.fixture
def mock_jira_issue():
    issue = Mock()
    issue.key = "TEST-123"
    issue.fields.summary = "Test Issue"
    issue.fields.description = "Test Description"
    issue.fields.created = datetime.now()
    issue.fields.updated = datetime.now()
    return issue

@pytest.fixture
def mock_jira_epic(mock_jira_issue):
    epic = mock_jira_issue
    epic.fields.customfield_10014 = "Epic Name"
    link1, link2 = Mock(), Mock()
    link1.outwardIssue.key = "TEST-124"
    link2.outwardIssue.key = "TEST-125"
    epic.fields.issuelinks = [link1, link2]
    return epic

@pytest.mark.asyncio
async def test_get_task(mock_jira_issue):
    with patch('app.services.jira.get_jira_client') as mock_client:
        mock_client.return_value.issue.return_value = mock_jira_issue
        task = await get_task("TEST-123")
        assert task is not None
        assert task.key == "TEST-123"
        assert task.summary == "Test Issue"

@pytest.mark.asyncio
async def test_get_epic(mock_jira_epic):
    with patch('app.services.jira.get_jira_client') as mock_client:
        mock_client.return_value.issue.return_value = mock_jira_epic
        epic = await get_epic("TEST-123")
        assert epic is not None
        assert epic.key == "TEST-123"
        assert epic.name == "Epic Name"
        assert len(epic.tasks) == 2
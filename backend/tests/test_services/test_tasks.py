import pytest
from datetime import datetime
from unittest.mock import Mock, ANY

from app.services.tasks import TasksService
from app.schemas.create_task import CreateTaskRequest, TaskPriority

@pytest.fixture
def mock_jira(mocker):
    mock = Mock()
    mock.create_issue.return_value = Mock(
        key="PROJ-123",
        raw={"id": "10000", "key": "PROJ-123"}
    )
    mocker.patch('app.services.tasks.get_jira_client', return_value=mock)
    return mock

def test_create_task_minimal(mock_jira):
    """Test creating task with minimal required fields"""
    # Configure mock return value
    mock_jira.create_issue.return_value = Mock(
        key="PROJ-123",
        raw={
            "key": "PROJ-123",
            "id": "10000",
            "self": "https://jira.example.com/rest/api/2/issue/10000"
        }
    )
    mock_jira.issue.return_value = mock_jira.create_issue.return_value

    service = TasksService()
    request = CreateTaskRequest(
        project_key="PROJ",
        summary="Test task"
    )

    result = service.create_task(request)

    assert result is not None
    assert result["key"] == "PROJ-123"
    mock_jira.create_issue.assert_called_once()

def test_create_task_full(mock_jira):
    """Test creating task with all fields"""
    # Configure mock return value
    mock_jira.create_issue.return_value = Mock(
        key="PROJ-123",
        raw={
            "key": "PROJ-123",
            "id": "10000",
            "self": "https://jira.example.com/rest/api/2/issue/10000",
            "fields": {
                "summary": "Test task",
                "description": "Test description", 
                "priority": {"name": "High"},
                "duedate": "2024-12-31",
                "timetracking": {"originalEstimate": "8h"},
                "customfield_10601": "PROJ-100",
                "labels": ["test"],
                "assignee": {"name": "john.doe"}
            }
        }
    )
    mock_jira.issue.return_value = mock_jira.create_issue.return_value

    service = TasksService()
    request = CreateTaskRequest(
        project_key="PROJ",
        summary="Test task",
        description="Test description",
        priority=TaskPriority.HIGH,
        due_date=datetime(2024, 12, 31),
        estimate=8.0,
        epic_link="PROJ-100",
        labels=["test"],
        assignee="john.doe"
    )

    result = service.create_task(request)

    assert result is not None
    assert result["key"] == "PROJ-123"
    mock_jira.create_issue.assert_called_once()
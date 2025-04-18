import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from datetime import datetime
from app.main import app
from app.schemas.task import TaskSchema
from app.schemas.create_task import TaskPriority

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_jira_client(mocker):
    """Mock JIRA client at the service level"""
    mock = Mock()
    mock.create_issue.return_value = Mock(
        key="PROJ-123",
        raw={
            "id": "10000",
            "key": "PROJ-123",
            "self": "https://jira.example.com/rest/api/2/issue/10000"
        }
    )
    mock.project.return_value = Mock(
        issueTypes=[
            Mock(id="10000", name="Engineer"),
            Mock(id="10001", name="Bug")
        ]
    )
    mocker.patch('app.services.tasks.get_jira_client', return_value=mock)
    return mock

@pytest.fixture
def mock_task():
    return TaskSchema(
        key="TEST-123",
        summary="Test Task",
        description="Test Description",
        created=datetime.now(),
        updated=datetime.now()
    )

@pytest.fixture
def mock_tasks_service(mocker):
    """Mock TasksService"""
    mock = Mock()
    mock.create_task.return_value = {
        "id": "10000",
        "key": "PROJ-123",
        "self": "https://jira.example.com/rest/api/2/issue/10000"
    }
    mock.get_task_types.return_value = [
        {"id": "10000", "name": "Engineer"},
        {"id": "10001", "name": "Bug"}
    ]
    mocker.patch('app.api.v1.tasks.TasksService', return_value=mock)
    mocker.patch('app.api.v1.tasks.get_tasks_service', return_value=mock)
    return mock

def test_read_task_success(mock_task):
    with patch('app.api.v1.tasks.get_task', return_value=mock_task):  # Changed path
        response = client.get("/api/v1/tasks/TEST-123")
        assert response.status_code == 200
        assert response.json()["key"] == "TEST-123"

def test_read_task_not_found():
    with patch('app.api.v1.tasks.get_task', return_value=None) as mock_get_task:
        print(f"DEBUG: Mock configured: {mock_get_task}")  # Debug print
        response = client.get("/api/v1/tasks/INVALID-123")
        print(f"DEBUG: Response received: {response.status_code}")  # Debug print
        print(f"DEBUG: Response body: {response.text}")  # Debug print
        assert response.status_code == 404

def test_read_task_error():
    with patch('app.api.v1.tasks.get_task', side_effect=Exception("JIRA Error")):  # Changed path
        response = client.get("/api/v1/tasks/TEST-123")
        assert response.status_code == 500

def test_create_task_minimal(mock_tasks_service):
    """Test creating task with minimal fields"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "project_key": "PROJ",
            "summary": "Test task"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "PROJ-123"
    mock_tasks_service.create_task.assert_called_once()

def test_create_task_full(mock_tasks_service):
    """Test creating task with all fields"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "project_key": "PROJ",
            "summary": "Test task",
            "description": "Test description",
            "issue_type": "Engineer",
            "priority": TaskPriority.HIGH.value,
            "due_date": "2024-12-31T00:00:00Z",
            "estimate": 8.0,
            "epic_link": "PROJ-100",
            "labels": ["test"],
            "assignee": "john.doe",
            "reporter": "jane.doe"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "PROJ-123"

def test_get_task_types(mock_tasks_service):
    """Test getting task types"""
    response = client.get("/api/v1/tasks/types/PROJ")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Engineer"
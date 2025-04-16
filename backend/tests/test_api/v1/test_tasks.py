import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime
from app.main import app
from app.schemas.task import TaskSchema

client = TestClient(app)

@pytest.fixture
def mock_task():
    return TaskSchema(
        key="TEST-123",
        summary="Test Task",
        description="Test Description",
        created=datetime.now(),
        updated=datetime.now()
    )

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
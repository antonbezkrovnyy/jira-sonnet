import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from app.schemas.create_task import TaskPriority

from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_jira_client(mocker):
    """Mock JIRA client for integration tests"""
    mock = Mock()
    
    # Create proper response dictionary
    issue_response = {
        "id": "10000",
        "key": "LOGIQPROD-123",
        "self": "https://jira.example.com/rest/api/2/issue/10000",
        "fields": {
            "summary": "Test Task",
            "description": "Test Description",
            "issuetype": {"name": "Engineer"},
            "priority": {"name": "High"},
            "duedate": "2024-12-31",
            "timetracking": {"originalEstimate": "8h"},
            "customfield_10601": "LOGIQPROD-100"
        }
    }

    # Configure mock
    mock_issue = Mock()
    mock_issue.raw = issue_response
    mock_issue.key = "LOGIQPROD-123"

    mock.create_issue.return_value = mock_issue
    mock.issue.return_value = mock_issue

    # Mock issue types correctly
    issue_type_engineer = Mock()
    issue_type_engineer.id = "10000"
    issue_type_engineer.name = "Engineer"

    issue_type_bug = Mock()
    issue_type_bug.id = "10001" 
    issue_type_bug.name = "Bug"

    mock.project.return_value = Mock(
        issueTypes=[issue_type_engineer, issue_type_bug]
    )

    mocker.patch('app.services.tasks.get_jira_client', return_value=mock)
    return mock

def test_create_task_minimal_integration():
    """Test creating task with minimal fields - integration test"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "project_key": "LOGIQPROD",
            "summary": "Test Task"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "LOGIQPROD-123"

def test_create_task_full_integration():
    """Test creating task with all fields - integration test"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "project_key": "LOGIQPROD",
            "summary": "Test Task",
            "description": "Test Description",
            "issue_type": "Engineer",
            "priority": "High",
            "due_date": "2024-12-31T00:00:00Z",
            "estimate": 8.0,
            "epic_link": "LOGIQPROD-100",
            "labels": ["test", "integration"],
            "assignee": "john.doe"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "LOGIQPROD-123"
    assert data["fields"]["customfield_10601"] == "LOGIQPROD-100"
    assert data["fields"]["timetracking"]["originalEstimate"] == "8h"

def test_get_task_types_integration():
    """Test getting task types - integration test"""
    response = client.get("/api/v1/tasks/types/LOGIQPROD")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(t["name"] == "Engineer" for t in data)
    assert any(t["name"] == "Bug" for t in data)

def test_create_task_error_handling():
    """Test error handling in task creation"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "project_key": "INVALID",
            "summary": ""  # Invalid empty summary
        }
    )
    
    assert response.status_code == 422  # Validation error
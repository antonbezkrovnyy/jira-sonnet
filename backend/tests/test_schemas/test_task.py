from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.task import TaskSchema

def test_valid_task():
    task_data = {
        "key": "PROJ-123",
        "created": datetime.now(),
        "updated": datetime.now(),
        "summary": "Test task",
        "description": "Test description",
        "assignee": "user@example.com",
        "due_date": datetime.now(),
        "epic_key": "PROJ-100",
        "labels": ["bug", "critical"]
    }
    task = TaskSchema(**task_data)
    assert task.key == "PROJ-123"
    assert task.summary == "Test task"

def test_invalid_task_key():
    with pytest.raises(ValidationError):
        TaskSchema(
            key="invalid",
            created=datetime.now(),
            updated=datetime.now(),
            summary="Test task"
        )
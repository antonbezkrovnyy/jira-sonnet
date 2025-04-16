from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.epic import EpicSchema

def test_valid_epic():
    epic_data = {
        "key": "PROJ-100",
        "created": datetime.now(),
        "updated": datetime.now(),
        "summary": "Test epic",
        "description": "Test description",
        "name": "Epic name",
        "tasks": ["PROJ-123", "PROJ-124"]
    }
    epic = EpicSchema(**epic_data)
    assert epic.key == "PROJ-100"
    assert len(epic.tasks) == 2

def test_invalid_epic_name():
    with pytest.raises(ValidationError):
        EpicSchema(
            key="PROJ-100",
            created=datetime.now(),
            updated=datetime.now(),
            summary="Test epic",
            name=""
        )
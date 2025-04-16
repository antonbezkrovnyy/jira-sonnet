import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.label import LabelSchema

def test_valid_label():
    """Test creating valid label schema"""
    now = datetime.now()
    label = LabelSchema(
        key="bug",
        name="Bug",
        description="Software bug",
        color="#ff0000",
        created=now,
        updated=now,
        used_in=["LOGIQPROD-123"]
    )
    assert label.key == "bug"
    assert label.name == "Bug"
    assert label.color == "#ff0000"
    assert len(label.used_in) == 1

def test_minimal_label():
    """Test creating minimal valid label"""
    now = datetime.now()
    label = LabelSchema(
        key="bug",
        name="Bug",
        created=now,
        updated=now
    )
    assert label.description is None
    assert label.color is None
    assert label.used_in == []

def test_invalid_label_missing_required():
    """Test label creation fails without required fields"""
    with pytest.raises(ValidationError):
        LabelSchema(
            description="Test label",
            created=datetime.now(),
            updated=datetime.now()
        )

def test_invalid_color_format():
    """Test validation of color format"""
    now = datetime.now()
    with pytest.raises(ValidationError):
        LabelSchema(
            key="bug",
            name="Bug",
            color="red",  # Invalid format
            created=now,
            updated=now
        )
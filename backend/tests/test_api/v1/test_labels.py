import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import patch, AsyncMock
from app.main import app
from app.schemas.label import LabelSchema

client = TestClient(app)

@pytest.fixture
def mock_label():
    """Create mock label data"""
    now = datetime.now()
    return LabelSchema(
        key="bug",
        name="Bug",
        description="Software bug",
        created=now,
        updated=now,
        used_in=["LOGIQPROD-123"]
    )

def test_read_label_success(mock_label):
    """Test successful label retrieval"""
    async def mock_get_label(*args, **kwargs):
        return mock_label
        
    with patch('app.api.v1.labels.get_label', mock_get_label):
        response = client.get("/api/v1/labels/bug")
        assert response.status_code == 200
        data = response.json()
        assert data["key"] == "bug"
        assert data["name"] == "Bug"
        assert "LOGIQPROD-123" in data["used_in"]

def test_read_label_not_found():
    """Test label not found response"""
    async def mock_get_label(*args, **kwargs):
        return None
        
    with patch('app.api.v1.labels.get_label', mock_get_label):
        response = client.get("/api/v1/labels/nonexistent")
        assert response.status_code == 404

def test_list_labels_success(mock_label):
    """Test successful labels list retrieval"""
    async def mock_get_project_labels(*args, **kwargs):
        return [mock_label]
        
    with patch('app.api.v1.labels.get_project_labels', mock_get_project_labels):
        response = client.get("/api/v1/labels/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["key"] == "bug"

def test_list_labels_empty():
    """Test empty labels list"""
    async def mock_get_project_labels(*args, **kwargs):
        return []
        
    with patch('app.api.v1.labels.get_project_labels', mock_get_project_labels):
        response = client.get("/api/v1/labels/")
        assert response.status_code == 200
        assert response.json() == []
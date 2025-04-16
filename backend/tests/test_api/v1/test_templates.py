import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from datetime import datetime
from app.main import app
from app.schemas.checklist import ChecklistType, ChecklistTemplate

client = TestClient(app)

@pytest.fixture
def mock_template():
    """Create mock template for tests"""
    return ChecklistTemplate(
        key="standard",
        name="Standard Template",
        description="Standard checklist template",
        version="1.0",
        type=ChecklistType.DOR,
        content="* Test item 1\n* Test item 2"
    )

@pytest.fixture
def mock_template_service():
    """Create mock template service"""
    with patch('app.api.v1.templates.get_template_service') as mock:
        service = Mock()
        mock.return_value = service
        yield service

def test_list_templates_success(mock_template, mock_template_service, caplog):
    """Test successful template listing"""
    mock_template_service.get_templates.return_value = [mock_template]
    
    response = client.get("/api/v1/templates/dor")
    print(f"Response: {response.status_code} - {response.text}")  # Debug output
    
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) == 1
    assert templates[0]["key"] == "standard"
    assert templates[0]["name"] == "Standard Template"

def test_list_templates_empty(mock_template_service):
    """Test empty templates list"""
    mock_template_service.get_templates.return_value = []
    
    response = client.get("/api/v1/templates/dor")
    assert response.status_code == 404
    assert "No dor templates found" in response.json()["detail"]

def test_get_template_success(mock_template, mock_template_service):
    """Test getting specific template"""
    mock_template_service.get_template.return_value = mock_template
    
    response = client.get("/api/v1/templates/dor/standard")
    assert response.status_code == 200
    
    template = response.json()
    assert template["key"] == "standard"
    assert template["name"] == "Standard Template"
    assert template["content"] == "* Test item 1\n* Test item 2"

def test_get_template_not_found(mock_template_service):
    """Test getting non-existent template"""
    mock_template_service.get_template.return_value = None
    
    response = client.get("/api/v1/templates/dor/nonexistent")
    assert response.status_code == 404
    assert "Template nonexistent not found" in response.json()["detail"]

def test_update_template_success(mock_template, mock_template_service):
    """Test successful template update"""
    mock_template_service.update_template.return_value = mock_template
    
    update_data = {
        "name": "Updated Template",
        "description": "Updated description",
        "content": "* Updated item 1\n* Updated item 2",
        "version": "1.1"
    }
    
    response = client.put("/api/v1/templates/dor/standard", json=update_data)
    assert response.status_code == 200
    
    template = response.json()
    assert template["name"] == "Standard Template"
    assert template["version"] == "1.0"

def test_update_template_not_found(mock_template_service):
    """Test updating non-existent template"""
    mock_template_service.update_template.return_value = None
    
    update_data = {
        "name": "Updated Template",
        "description": "Updated description",
        "content": "* Updated item 1",
        "version": "1.1"
    }
    
    response = client.put("/api/v1/templates/dor/nonexistent", json=update_data)
    assert response.status_code == 404
    assert "Template nonexistent not found" in response.json()["detail"]

def test_delete_template_success(mock_template_service):
    """Test successful template deletion"""
    mock_template_service.delete_template.return_value = True
    
    response = client.delete("/api/v1/templates/dor/standard")
    assert response.status_code == 200
    assert response.json() is True

def test_delete_template_not_found(mock_template_service):
    """Test deleting non-existent template"""
    mock_template_service.delete_template.return_value = False
    
    response = client.delete("/api/v1/templates/dor/nonexistent")
    assert response.status_code == 404
    assert "Template nonexistent not found" in response.json()["detail"]
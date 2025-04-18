import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from app.main import app
from app.schemas.link import LinkType, ResourceType, TaskLink, ExternalLink

client = TestClient(app)

@pytest.fixture
def mock_links_service(mocker):
    """Mock LinksService"""
    mock = Mock()
    # Create proper TaskLink objects for return values
    mock.get_task_links.return_value = [
        TaskLink(
            id="10000",
            type=LinkType.BLOCKS,
            source="PROJ-123",
            target="PROJ-456"
        )
    ]
    mock.create_task_link.return_value = TaskLink(
        id="10001",
        type=LinkType.BLOCKS,
        source="PROJ-123",
        target="PROJ-456"
    )
    # Fix patch path to point to endpoint dependency
    mocker.patch('app.api.v1.links.LinksService', return_value=mock)
    mocker.patch('app.api.v1.links.get_links_service', return_value=mock)
    return mock

@pytest.fixture
def mock_external_links_service(mocker):
    """Mock ExternalLinksService"""
    mock = Mock()
    # Create proper ExternalLink objects for return values
    mock.get_external_links.return_value = [
        ExternalLink(
            id="10000",
            type=ResourceType.CONFLUENCE,
            source="PROJ-123",
            target="Wiki Page",  # Added target field
            title="Wiki Page",
            url="https://confluence.example.com/page"
        )
    ]
    mock.create_external_link.return_value = ExternalLink(
        id="10001",
        type=ResourceType.CONFLUENCE,
        source="PROJ-123",
        target="New Page",  # Added target field
        title="New Page",
        url="https://confluence.example.com/new-page"
    )
    # Fix patch path to point to endpoint dependency
    mocker.patch('app.api.v1.links.ExternalLinksService', return_value=mock)
    mocker.patch('app.api.v1.links.get_external_links_service', return_value=mock)
    return mock

def test_get_task_links(mock_links_service):
    """Test getting task links"""
    response = client.get("/api/v1/tasks/PROJ-123/links")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["source"] == "PROJ-123"
    mock_links_service.get_task_links.assert_called_once_with("PROJ-123")

def test_create_task_link(mock_links_service):
    """Test creating task link"""
    response = client.post(
        "/api/v1/tasks/PROJ-123/links",
        json={
            "type": "blocks",
            "target": "PROJ-456"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "PROJ-123"
    assert data["target"] == "PROJ-456"
    mock_links_service.create_task_link.assert_called_once()

def test_get_external_links(mock_external_links_service):
    """Test getting external links"""
    response = client.get("/api/v1/tasks/PROJ-123/external-links")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Wiki Page"
    mock_external_links_service.get_external_links.assert_called_once_with("PROJ-123")

def test_create_external_link(mock_external_links_service):
    """Test creating external link"""
    test_url = "https://confluence.example.com/new-page"
    
    response = client.post(
        "/api/v1/tasks/PROJ-123/external-links",
        json={
            "type": ResourceType.CONFLUENCE.value,
            "title": "New Page",
            "url": test_url,
            "target": "New Page"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Page"
    assert data["url"] == test_url
    
    # Get the actual url object that was passed to the service
    actual_calls = mock_external_links_service.create_external_link.call_args_list
    assert len(actual_calls) == 1
    
    call_kwargs = actual_calls[0].kwargs
    assert call_kwargs["task_key"] == "PROJ-123"
    assert call_kwargs["title"] == "New Page" 
    assert str(call_kwargs["url"]) == test_url  # Compare string representation
    assert call_kwargs["link_type"] == ResourceType.CONFLUENCE

def test_create_task_link_error(mock_links_service):
    """Test error handling when creating task link"""
    # Setup mock to return None (error)
    mock_links_service.create_task_link.return_value = None
    
    # Make request
    response = client.post(
        "/api/v1/tasks/PROJ-123/links",
        json={
            "type": "blocks",
            "target": "PROJ-456"
        }
    )
    
    # Verify error response
    assert response.status_code == 400
    assert response.json()["detail"] == "Failed to create link"
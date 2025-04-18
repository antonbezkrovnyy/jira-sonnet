import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.link import (
    LinkType, 
    ResourceType,
    TaskLink,
    ExternalLink,
    CreateTaskLinkRequest,
    CreateExternalLinkRequest
)

def test_valid_task_link():
    """Test creating valid task link"""
    link_data = {
        "id": "10000",
        "type": "blocks",
        "source": "PROJ-123",
        "target": "PROJ-456",
        "created": datetime.now(),
        "updated": datetime.now()
    }
    link = TaskLink(**link_data)
    assert link.id == "10000"
    assert link.type == LinkType.BLOCKS
    assert link.source == "PROJ-123"
    assert link.target == "PROJ-456"

def test_invalid_task_link_type():
    """Test task link with invalid link type"""
    link_data = {
        "id": "10000",
        "type": "invalid_type",  # Invalid type
        "source": "PROJ-123",
        "target": "PROJ-456",
        "created": datetime.now()
    }
    with pytest.raises(ValidationError) as exc:
        TaskLink(**link_data)
    assert "type" in str(exc.value)

def test_valid_external_link():
    """Test creating valid external link"""
    link_data = {
        "id": "10001",
        "type": "confluence",
        "source": "PROJ-123",
        "target": "12345",
        "title": "Design Document",
        "url": "https://confluence.company.com/page/12345",
        "created": datetime.now()
    }
    link = ExternalLink(**link_data)
    assert link.id == "10001"
    assert link.type == ResourceType.CONFLUENCE
    assert link.title == "Design Document"
    assert str(link.url) == "https://confluence.company.com/page/12345"

def test_invalid_external_link_url():
    """Test external link with invalid URL"""
    link_data = {
        "id": "10001",
        "type": "confluence",
        "source": "PROJ-123",
        "target": "12345",
        "title": "Design Document",
        "url": "not-a-url",  # Invalid URL
        "created": datetime.now()
    }
    with pytest.raises(ValidationError) as exc:
        ExternalLink(**link_data)
    assert "url" in str(exc.value)

def test_create_task_link_request():
    """Test task link creation request"""
    request_data = {
        "type": "relates to",
        "target": "PROJ-789"
    }
    request = CreateTaskLinkRequest(**request_data)
    assert request.type == LinkType.RELATES_TO
    assert request.target == "PROJ-789"

def test_create_external_link_request():
    """Test external link creation request"""
    request_data = {
        "type": "web",
        "target": "doc-id",
        "title": "External Doc",
        "url": "https://example.com/doc"
    }
    request = CreateExternalLinkRequest(**request_data)
    assert request.type == ResourceType.WEB
    assert request.title == "External Doc"
    assert str(request.url) == "https://example.com/doc"
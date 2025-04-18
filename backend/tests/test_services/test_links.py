import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from app.services.links import LinksService
from app.schemas.link import LinkType, TaskLink

@pytest.fixture
def mock_jira():
    """Create mock JIRA client"""
    with patch('app.services.links.get_jira_client') as mock:
        client = Mock()
        mock.return_value = client
        yield client

@pytest.fixture
def mock_issue():
    """Create mock JIRA issue with links"""
    issue = Mock()
    
    # Create mock link
    link = Mock()
    link.id = "10000"
    link.type = Mock()
    link.type.name = "Blocks"
    link.type.outward = "blocks"
    link.type.inward = "is blocked by"
    
    # Create mock target issue
    target = Mock()
    target.key = "PROJ-456"
    link.outwardIssue = target
    
    # Set created/updated dates
    link.created = datetime.now()
    link.updated = datetime.now()
    
    # Add link to issue
    issue.fields.issuelinks = [link]
    return issue

def test_get_task_links(mock_jira, mock_issue):
    """Test getting task links"""
    # Setup
    mock_jira.issue.return_value = mock_issue
    service = LinksService()
    
    # Execute
    links = service.get_task_links("PROJ-123")
    
    # Verify
    assert len(links) == 1
    link = links[0]
    assert link.id == "10000"
    assert link.type == "blocks"
    assert link.source == "PROJ-123"
    assert link.target == "PROJ-456"
    mock_jira.issue.assert_called_once_with("PROJ-123")

def test_create_task_link(mock_jira):
    """Test creating task link"""
    # Setup
    mock_jira.create_issue_link.return_value = None  # JIRA doesn't return link object
    service = LinksService()

    # Execute
    link = service.create_task_link(
        source="PROJ-123",
        link_type=LinkType.BLOCKS,
        target="PROJ-456"
    )

    # Verify
    assert link is not None
    assert link.id == "new"  # We use "new" as placeholder
    assert link.source == "PROJ-123"
    assert link.target == "PROJ-456"
    assert link.type == LinkType.BLOCKS
    mock_jira.create_issue_link.assert_called_once()

def test_get_task_links_error(mock_jira):
    """Test error handling when getting links"""
    # Setup
    mock_jira.issue.side_effect = Exception("JIRA error")
    service = LinksService()
    
    # Execute
    links = service.get_task_links("PROJ-123")
    
    # Verify
    assert links == []
    mock_jira.issue.assert_called_once_with("PROJ-123")

def test_create_task_link_error(mock_jira):
    """Test error handling when creating link"""
    # Setup
    mock_jira.create_issue_link.side_effect = Exception("JIRA error")
    service = LinksService()
    
    # Execute
    link = service.create_task_link(
        source="PROJ-123",
        link_type=LinkType.BLOCKS,
        target="PROJ-456"
    )
    
    # Verify
    assert link is None
    mock_jira.create_issue_link.assert_called_once()
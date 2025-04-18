import pytest
from datetime import datetime
from app.services.links import LinksService
from app.schemas.link import LinkType

@pytest.fixture
def integration_env():
    """Setup test data for integration tests"""
    return {
        'source_task': 'LOGIQPROD-635',  # Существующая задача
        'target_task': 'LOGIQPROD-634',  # Эпик, к которому привязана задача
        'link_type': LinkType.RELATES_TO
    }

@pytest.mark.integration
def test_get_task_links(integration_env):
    """Test getting links from real JIRA task"""
    service = LinksService()
    links = service.get_task_links(integration_env['source_task'])
    
    # We may have 0 links initially
    assert isinstance(links, list)
    
    # If we have links, verify structure
    for link in links:
        assert link.source == integration_env['source_task']
        assert link.id is not None
        assert link.type is not None
        assert link.target is not None

@pytest.mark.integration
def test_create_and_get_task_link(integration_env):
    """Test creating and then getting link"""
    service = LinksService()
    
    # Create link
    link = service.create_task_link(
        source=integration_env['source_task'],
        link_type=integration_env['link_type'],
        target=integration_env['target_task']
    )
    print(f"Created link: {link}")
    # Verify link created
    assert link is not None
    assert link.source == integration_env['source_task']
    assert link.target == integration_env['target_task']
    assert link.type == integration_env['link_type']
    assert link.id == "new"
    
    # Get links and verify our link exists
    links = service.get_task_links(integration_env['source_task'])
    assert any(l.target == integration_env['target_task'] for l in links)
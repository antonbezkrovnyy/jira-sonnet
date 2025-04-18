import pytest
import time
from app.services.external_links import ExternalLinksService
from app.schemas.link import ResourceType

@pytest.fixture
def integration_env():
    """Setup test data for integration tests"""
    return {
        'task_key': 'LOGIQPROD-635',
        'link_title': 'Test Documentation',
        'link_url': f'https://example.com/docs?t={int(time.time())}',  # Unique URL
        'link_type': ResourceType.WEB
    }

@pytest.mark.integration
def test_create_and_get_external_link(integration_env):
    """Test creating and getting external link"""
    service = ExternalLinksService()
    
    # Create link
    link = service.create_external_link(
        task_key=integration_env['task_key'],
        title=integration_env['link_title'],
        url=integration_env['link_url'],
        link_type=integration_env['link_type']
    )
    
    # Verify link created
    assert link is not None
    assert link.source == integration_env['task_key']
    assert link.title == integration_env['link_title']
    assert str(link.url) == integration_env['link_url']  # Convert URL to string
    assert link.type == integration_env['link_type']
    
    # Get links and verify
    links = service.get_external_links(integration_env['task_key'])
    assert any(
        str(l.url) == integration_env['link_url']  # Convert URL to string 
        for l in links
    ), "Created link not found in results"
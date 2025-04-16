import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from app.services.labels import get_label, get_project_labels

@pytest.fixture
def mock_jira_issue():
    """Create mock JIRA issue with labels"""
    issue = Mock()
    issue.key = "LOGIQPROD-123"
    issue.fields.labels = ["bug", "critical"]
    issue.fields.created = datetime.now()
    issue.fields.updated = datetime.now()
    return issue

@pytest.mark.asyncio
async def test_get_label(mock_jira_issue):
    """Test getting single label"""
    with patch('app.services.labels.get_jira_client') as mock_client:
        # Setup mock
        mock_client.return_value.search_issues.return_value = [mock_jira_issue]
        
        # Test
        label = await get_label('bug')
        
        # Assert
        assert label is not None
        assert label.key == 'bug'
        assert label.name == 'Bug'
        assert 'LOGIQPROD-123' in label.used_in

@pytest.mark.asyncio
async def test_get_project_labels(mock_jira_issue):
    """Test getting all project labels"""
    with patch('app.services.labels.get_jira_client') as mock_client:
        mock_client.return_value.search_issues.return_value = [mock_jira_issue]
        
        labels = await get_project_labels()
        
        assert len(labels) == 2  # bug and critical
        assert any(l.key == 'bug' for l in labels)
        assert any(l.key == 'critical' for l in labels)

@pytest.mark.asyncio
async def test_get_label_not_found():
    """Test getting non-existent label"""
    with patch('app.services.labels.get_jira_client') as mock_client:
        mock_client.return_value.search_issues.return_value = []
        label = await get_label('nonexistent')
        assert label is None
import os
from app.core.config import get_settings

def test_get_settings():
    # Arrange
    os.environ['JIRA_URL'] = 'http://test.com'
    os.environ['JIRA_USER'] = 'test@test.com'
    os.environ['JIRA_TOKEN'] = 'test-token'
    
    # Act
    settings = get_settings()
    
    # Assert
    assert settings['jira_url'] == 'http://test.com'
    assert settings['jira_user'] == 'test@test.com'
    assert settings['jira_token'] == 'test-token'
import pytest
import os

@pytest.fixture(autouse=True)
def env_setup():
    os.environ['JIRA_URL'] = 'http://test.com'
    os.environ['JIRA_USER'] = 'test@test.com'
    os.environ['JIRA_TOKEN'] = 'test-token'
    yield
    os.environ.pop('JIRA_URL', None)
    os.environ.pop('JIRA_USER', None)
    os.environ.pop('JIRA_TOKEN', None)
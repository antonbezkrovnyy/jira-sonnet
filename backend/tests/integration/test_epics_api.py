import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.jira import get_jira_client  # Add JIRA client import

client = TestClient(app)

@pytest.fixture
def integration_env():
    """Setup test data for integration tests"""
    return {
        'project_key': 'LOGIQPROD',  # Add this explicitly
        'epic_key': 'LOGIQPROD-634',
        'task_key': 'LOGIQPROD-635',
        'issue_type': 'Engineer',
        'epic_name': 'Клиент ГПНА',
        'epic_summary': 'Клиент Газпромнефть Автоматизация',
        'task_summary': 'Ошибка инсталляции ансибл логик у гпна'
    }

@pytest.mark.integration
def test_jira_epic_data(integration_env):
    """Test raw JIRA data before testing API"""
    # Get JIRA client
    jira = get_jira_client()
    
    # Get epic directly from JIRA
    epic = jira.issue(integration_env['epic_key'])
    
    # Verify epic data
    assert epic.key == integration_env['epic_key']
    assert getattr(epic.fields, 'customfield_10604', None) == integration_env['epic_name']
    assert epic.fields.summary == integration_env['epic_summary']
    
    # Get linked tasks using epic key
    tasks = jira.search_issues(f'"Epic Link" = {integration_env["epic_key"]} AND issuetype = Engineer')
    task_keys = [task.key for task in tasks]
    
    # Verify task data
    assert integration_env['task_key'] in task_keys
    task = next(task for task in tasks if task.key == integration_env['task_key'])
    assert task.fields.summary == integration_env['task_summary']

@pytest.mark.integration
def test_connection_data(integration_env):
    """Verify we have correct test data"""
    print(f"Debug env: {integration_env}")  # Debug print
    assert integration_env['project_key'] == 'LOGIQPROD'
    assert integration_env['epic_key'] == 'LOGIQPROD-634'  # Updated to match .env
    assert integration_env['task_key'] == 'LOGIQPROD-635'
    assert integration_env['issue_type'] == 'Engineer'

@pytest.mark.integration
def test_get_epic(integration_env):
    response = client.get(f"/api/v1/epics/{integration_env['epic_key']}")
    assert response.status_code == 200
    data = response.json()
    
    # Check correct fields
    assert data["key"] == integration_env['epic_key']
    assert data["name"] == integration_env['epic_name']  # customfield_10604
    assert data["summary"] == integration_env['epic_summary']
    
    # Check if task is linked
    assert integration_env['task_key'] in data["tasks"]

@pytest.mark.integration
def test_get_epic_tasks(integration_env):
    response = client.get(f"/api/v1/epics/{integration_env['epic_key']}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    
    # Check if our known task is in the list
    task = next((t for t in tasks if t["key"] == integration_env['task_key']), None)
    assert task is not None
    assert task["summary"] == integration_env['task_summary']
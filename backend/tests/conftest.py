import pytest
import os
from dotenv import load_dotenv

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )

@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """Load environment variables for tests"""
    try:
        load_dotenv('.env.test.integration')
        # Debug print to verify loading
        print(f"Loaded TEST_PROJECT_KEY: {os.getenv('TEST_PROJECT_KEY')}")
        print(f"Loaded TEST_EPIC_KEY: {os.getenv('TEST_EPIC_KEY')}")
    except Exception as e:
        print(f"Error loading .env.test.integration: {e}")

@pytest.fixture(scope="session")
def integration_env():
    """Provide test data for integration tests"""
    return {
        'project_key': os.getenv('TEST_PROJECT_KEY'),
        'epic_key': 'LOGIQPROD-634',
        'task_key': 'LOGIQPROD-635',
        'issue_type': os.getenv('TEST_ISSUE_TYPE', 'Engineer'),
        'epic_name': 'Клиент ГПНА',  # From customfield_10604
        'epic_summary': 'Клиент Газпромнефть Автоматизация',
        'task_summary': 'Ошибка инсталляции ансибл логик у гпна'
    }

@pytest.fixture(autouse=True)
def env_setup():
    # Сохраняем оригинальные значения
    original_env = {
        'JIRA_URL': os.environ.get('JIRA_URL'),
        'JIRA_USER': os.environ.get('JIRA_USER'),
        'JIRA_TOKEN': os.environ.get('JIRA_TOKEN')
    }
    
    # Устанавливаем тестовые значения
    os.environ['JIRA_URL'] = 'https://jira.jet.su'
    os.environ['JIRA_USER'] = 'aa.bezkrovnyy'
    os.environ['JIRA_TOKEN'] = 'Tkf$5sqlbch7h2v'
    
    yield
    
    # Восстанавливаем оригинальные значения
    for key, value in original_env.items():
        if value is not None:
            os.environ[key] = value
        else:
            os.environ.pop(key, None)
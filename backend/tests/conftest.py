import pytest
import os

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
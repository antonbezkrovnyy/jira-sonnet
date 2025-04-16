from datetime import datetime
import pytest
from unittest.mock import Mock, patch
from app.services.jira import get_task, get_epic

@pytest.fixture
def mock_jira_issue():
    issue = Mock()
    issue.key = "TEST-123"
    issue.fields.summary = "Test Issue"
    issue.fields.description = "Test Description"
    issue.fields.created = datetime.now()
    issue.fields.updated = datetime.now()
    return issue

@pytest.fixture
def mock_jira_epic(mock_jira_issue):
    epic = mock_jira_issue
    # Правильное поле для имени эпика
    epic.fields.customfield_10604 = "Epic Name"
    
    # Создаем связанные задачи
    task1, task2 = Mock(), Mock()
    task1.key = "TEST-124"
    task2.key = "TEST-125"
    
    # Настраиваем возвращаемое значение для search_issues
    mock_search = Mock()
    mock_search.return_value = [task1, task2]
    epic.search_issues = mock_search
    
    return epic

@pytest.mark.asyncio
async def test_get_task(mock_jira_issue):
    with patch('app.services.jira.get_jira_client') as mock_client:
        mock_client.return_value.issue.return_value = mock_jira_issue
        task = await get_task("TEST-123")
        assert task is not None
        assert task.key == "TEST-123"
        assert task.summary == "Test Issue"

@pytest.mark.asyncio
async def test_get_epic(mock_jira_epic):
    with patch('app.services.jira.get_jira_client') as mock_client:
        # Настраиваем мок для получения эпика
        mock_client.return_value.issue.return_value = mock_jira_epic
        
        # Настраиваем мок для поиска задач
        mock_client.return_value.search_issues.return_value = [
            Mock(key="TEST-124"),
            Mock(key="TEST-125")
        ]
        
        # Вызываем тестируемую функцию
        epic = await get_epic("TEST-123")
        
        # Проверяем результат
        assert epic is not None
        assert epic.key == "TEST-123"
        assert epic.name == "Epic Name"  # Проверяем имя эпика из customfield_10604
        assert len(epic.tasks) == 2  # Проверяем количество связанных задач
        assert "TEST-124" in epic.tasks  # Проверяем ключи задач
        assert "TEST-125" in epic.tasks
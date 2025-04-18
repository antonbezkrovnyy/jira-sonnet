import os
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from dotenv import load_dotenv
import logging

from app.main import app
from app.schemas.create_task import TaskPriority
from app.services.tasks import TasksService

# Настройка логирования для тестов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load test integration environment
load_dotenv("backend/.env.test.integration")

client = TestClient(app)

@pytest.mark.integration
def test_create_real_task():
    """Test creating real task in JIRA"""
    test_summary = f"[TEST] Integration Test Task {datetime.now().isoformat()}"
    test_date = datetime.now().isoformat()

    # Проверяем доступные поля в JIRA
    service = TasksService()
    logger.info("\nПроверяем доступные поля в JIRA:")
    fields = service.get_field_ids(os.getenv("TEST_TASK_KEY"))
    
    # Выводим все поля с epic и estimate в названии
    for name, field_id in fields.items():
        if any(keyword in name.lower() for keyword in ['epic', 'estimate', 'time']):
            logger.info(f"Field: {name}, ID: {field_id}")

    # Создаем задачу
    response = client.post(
        "/api/v1/tasks",
        json={
            "project_key": os.getenv("TEST_PROJECT_KEY"),
            "summary": test_summary,
            "description": "This task was created by integration test",
            "issue_type": "Engineer",
            "priority": TaskPriority.MEDIUM.value,
            "labels": ["test", "integration"],
            "due_date": test_date,
            "epic_link": os.getenv("TEST_EPIC_KEY"),
            "estimate": 4.0,
            "assignee": os.getenv("JIRA_USER")
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем и логируем результат
    logger.info("\nРезультат создания задачи:")
    logger.info(f"Task key: {data.get('key')}")
    
    fields = data.get("fields", {})
    epic_link = fields.get("customfield_10014")  # Epic Link field
    estimate = fields.get("timeoriginalestimate")
    
    logger.info(f"Epic link: {epic_link}")
    logger.info(f"Original estimate: {estimate}")
    
    # Проверяем через API JIRA
    created_issue = service.client.issue(data["key"])
    logger.info("\nПроверка через API JIRA:")
    logger.info(f"Epic Link: {getattr(created_issue.fields, 'customfield_10014', None)}")
    logger.info(f"Time Original Estimate: {getattr(created_issue.fields, 'timeoriginalestimate', None)}")

    assert data["key"].startswith(os.getenv("TEST_PROJECT_KEY"))
    
@pytest.mark.integration
def test_get_real_task_types():
    """Test getting real task types from JIRA project"""
    response = client.get(
        f"/api/v1/tasks/types/{os.getenv('TEST_PROJECT_KEY')}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(t["name"] == "Engineer" for t in data)
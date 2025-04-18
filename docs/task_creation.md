# Создание задач в JIRA

## Основные поля
При создании задачи в JIRA используются следующие поля:

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|-----------|---------|
| project_key | string | Да | Ключ проекта | "LOGIQPROD" |
| summary | string | Да | Название задачи | "Реализовать API" |
| issue_type | string | Нет | Тип задачи | "Engineer" |
| priority | string | Нет | Приоритет | "High" |
| description | string | Нет | Описание задачи | "Необходимо..." |
| assignee | string | Нет | Исполнитель | "john.doe" |

## Специальные поля
Для корректной работы со специальными полями используются следующие ID:

| Поле | ID в JIRA | Формат | Пример |
|------|------------|--------|---------|
| Epic Link | customfield_10601 | string | "LOGIQPROD-634" |
| Time Tracking | timetracking | {"originalEstimate": "Xh Ym"} | {"originalEstimate": "4h 30m"} |

## Примеры запросов

### Минимальный запрос
```json
{
    "project_key": "LOGIQPROD",
    "summary": "Test Task"
}
```

### Полный запрос
```json
{
    "project_key": "LOGIQPROD",
    "summary": "Test Task",
    "description": "Test Description",
    "issue_type": "Engineer",
    "priority": "High",
    "due_date": "2024-12-31T00:00:00Z",
    "estimate": 8.0,
    "epic_link": "LOGIQPROD-634",
    "labels": ["test", "integration"],
    "assignee": "john.doe"
}
```

## Особенности реализации

1. **Epic Link**
   - Используется поле `customfield_10601`
   - Передается напрямую ключ эпика
   - Проверяется существование эпика перед связью

2. **Time Tracking**
   - Используется встроенное поле `timetracking`
   - Время задается в часах через поле `estimate`
   - Автоматически конвертируется в формат "Xh Ym"

3. **Валидация**
   - Проверяется существование проекта
   - Проверяется корректность типа задачи
   - Проверяется формат всех полей

## Примеры кода

```python
from jira import JIRA
from datetime import datetime

# Создание простой задачи
response = client.post(
    "/api/v1/tasks",
    json={
        "project_key": "LOGIQPROD",
        "summary": "Test Task"
    }
)

# Создание задачи с эпиком и оценкой времени
response = client.post(
    "/api/v1/tasks",
    json={
        "project_key": "LOGIQPROD",
        "summary": "Test Task",
        "epic_link": "LOGIQPROD-634",
        "estimate": 4.5  # Будет преобразовано в "4h 30m"
    }
)
```

## Известные ограничения

1. Поля эпика и времени должны быть доступны в проекте
2. Пользователь должен иметь права на:
   - Создание задач в проекте
   - Просмотр эпиков
   - Установку времени
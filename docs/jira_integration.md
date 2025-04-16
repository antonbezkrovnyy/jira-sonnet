# Интеграция с JIRA

## Связь Epic-Task
Документация описывает принципы связи эпиков и задач в нашей интеграции с JIRA.

### Пользовательские поля
| Поле | ID в JIRA | Описание | Пример |
|------|------------|----------|---------|
| Epic Name | customfield_10604 | Отображаемое имя эпика | "Клиент ГПНА" |
| Epic Link | встроенное | Ссылка на ключ эпика в задачах | LOGIQPROD-634 |

### Структура данных

#### Объект Epic
```json
{
    "key": "LOGIQPROD-634",
    "summary": "Клиент Газпромнефть Автоматизация",
    "name": "Клиент ГПНА",
    "tasks": ["LOGIQPROD-635", "LOGIQPROD-636"]
}
```

#### Объект Task
```json
{
    "key": "LOGIQPROD-635",
    "summary": "Ошибка инсталляции ансибл логик у гпна",
    "epic_link": "LOGIQPROD-634"
}
```

### Запросы к API

#### Получение данных эпика
```python
# Получение эпика по ключу
epic = jira.issue("LOGIQPROD-634")

# Получение имени эпика
epic_name = getattr(epic.fields, 'customfield_10604', None)
```

#### Получение задач эпика
```sql
"Epic Link" = LOGIQPROD-634 AND issuetype = Engineer
```

### Интеграционное тестирование
Пример интеграционного теста для проверки связи эпик-задача:

```python
def test_jira_epic_data(integration_env):
    """Тестирование данных JIRA напрямую"""
    jira = get_jira_client()
    
    # Проверка данных эпика
    epic = jira.issue(integration_env['epic_key'])
    assert epic.key == integration_env['epic_key']
    assert getattr(epic.fields, 'customfield_10604', None) == integration_env['epic_name']
    
    # Проверка связанных задач
    tasks = jira.search_issues(f'"Epic Link" = {integration_env["epic_key"]} AND issuetype = Engineer')
    task_keys = [task.key for task in tasks]
    assert integration_env['task_key'] in task_keys
```

### REST API Endpoints

#### Получение эпика
```http
GET /api/v1/epics/{key}
```
Возвращает эпик со связанными задачами. Использует `customfield_10604` для имени эпика.

#### Получение задач эпика
```http
GET /api/v1/epics/{key}/tasks
```
Возвращает задачи, связанные с эпиком через Epic Link.

### Частые проблемы

1. **Epic Name vs Epic Link**
   - Epic Name (`customfield_10604`) - отображаемое имя
   - Epic Link - ссылка на ключ эпика в JQL

2. **Поиск задач**
   - Используйте `"Epic Link" = EPIC-KEY` в JQL
   - Не заключайте ключ эпика в кавычки
   - Всегда включайте `issuetype = Engineer`

### Настройка окружения
Необходимые переменные окружения:
```bash
JIRA_URL=https://jira.domain.com
JIRA_USER=username
JIRA_TOKEN=api-token
```

### Тестирование
Запуск интеграционных тестов:
```bash
cd backend
pytest tests/integration/test_epics_api.py -v -m integration
```
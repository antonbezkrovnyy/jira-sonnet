# Links API Design

## Назначение
API для управления связями задач с другими задачами и внешними ресурсами.

## Типы связей

### 1. Внутренние связи (JIRA)
- **blocks** - блокирует
- **is blocked by** - блокируется
- **relates to** - связана с
- **duplicates** - дублирует
- **is duplicated by** - дублируется

### 2. Внешние связи
- **confluence** - страница Confluence
- **web** - внешняя веб-ссылка
- **gdoc** - документ Google

## API Endpoints

### GET /api/v1/links/{task_key}
Получение всех связей задачи

**Параметры:**
- `task_key` (path) - ключ задачи
- `type` (query, optional) - фильтр по типу связи

**Ответ:**
```json
{
    "internal": [
        {
            "id": "string",
            "type": "blocks",
            "source": "TASK-123",
            "target": "TASK-456",
            "created": "2024-04-16T12:00:00Z",
            "updated": "2024-04-16T13:00:00Z"
        }
    ],
    "external": [
        {
            "id": "string",
            "type": "confluence",
            "source": "TASK-123",
            "target": "12345",
            "title": "Design Document",
            "url": "https://confluence.company.com/page/12345",
            "created": "2024-04-16T12:00:00Z"
        }
    ]
}
```

### POST /api/v1/links/{task_key}
Создание новой связи

**Тело запроса:**
```json
{
    "type": "blocks",
    "target": "TASK-456"
}
```
или
```json
{
    "type": "confluence",
    "target": "12345",
    "title": "Design Document",
    "url": "https://confluence.company.com/page/12345"
}
```

### DELETE /api/v1/links/{task_key}/{link_id}
Удаление связи

## Валидация

### Внутренние связи
1. Проверка существования задачи
2. Проверка прав доступа
3. Проверка на циклические зависимости
4. Валидация типа связи

### Внешние связи
1. Валидация URL
2. Проверка доступности ресурса
3. Валидация формата ссылки

## Обработка ошибок
- 400: Неверный запрос
- 401: Не авторизован
- 403: Нет прав доступа
- 404: Задача/связь не найдена
- 409: Конфликт (например, циклическая зависимость)
- 500: Внутренняя ошибка сервера

## Интеграция
- JIRA REST API для работы с задачами
- Confluence API для проверки страниц
- HTTP клиент для проверки внешних ссылок
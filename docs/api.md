# API Documentation

## Epics API

### GET /api/v1/epics/{key}
Получение эпика по ключу

**Response 200**:
```json
{
    "key": "LOGIQPROD-634",
    "name": "Клиент ГПНА",
    "summary": "Клиент Газпромнефть Автоматизация",
    "tasks": ["LOGIQPROD-635", "LOGIQPROD-636"]
}
```

### GET /api/v1/epics/{key}/tasks
Получение задач эпика

**Response 200**:
```json
[
    {
        "key": "LOGIQPROD-635",
        "summary": "Ошибка инсталляции ансибл логик у гпна"
    }
]
```

## Tasks API
...существующая документация...
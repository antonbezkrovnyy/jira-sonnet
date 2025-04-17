# Backend Documentation

## Структура проекта
```
backend/
├── app/
│   ├── main.py              # FastAPI приложение
│   ├── core/
│   │   ├── config.py        # Конфигурация
│   │   └── logging.py       # Логирование
│   ├── api/
│   │   └── v1/
│   │       ├── tasks.py     # Операции с задачами
│   │       ├── epics.py     # Операции с эпиками
│   │       ├── labels.py    # Операции с метками
│   │       ├── templates.py # Управление шаблонами DoR/DoD
│   │       └── links.py     # Операции со связями
│   ├── services/
│   │   ├── jira.py         # JIRA API клиент
│   │   ├── templates.py    # Управление шаблонами
│   │   ├── tasks.py       # Операции с задачами
│   │   └── labels.py      # Управление метками
│   └── schemas/           # Pydantic модели
       ├── task.py        
       ├── epic.py
       ├── label.py
       ├── checklist.py   # Модели для DoR/DoD
       └── link.py
├── checklists/           # Шаблоны DoR/DoD
│   ├── dor/             # Definition of Ready
│   └── dod/             # Definition of Done
```

## Основные компоненты

### API Endpoints (v1)
- `/api/v1/tasks/` - управление задачами
- `/api/v1/epics/` - работа с эпиками
- `/api/v1/labels/` - управление метками
- `/api/v1/templates/` - управление шаблонами DoR/DoD
- `/api/v1/links/` - управление ссылками

### Модели данных
Pydantic модели для валидации:
- **TaskSchema**: модель задачи
- **EpicSchema**: модель эпика
- **LabelSchema**: модель метки
- **ChecklistTemplate**: модель шаблона DoR/DoD
- **LinkSchema**: модель ссылки

### Хранение данных
- **checklists/**: Markdown файлы с шаблонами DoR/DoD
  - dor/: шаблоны Definition of Ready
  - dod/: шаблоны Definition of Done
- **settings/**: YAML файлы с настройками и метками

### Сервисы
- **JiraService**: работа с JIRA REST API
  - Получение задач и эпиков
  - Обновление задач
  - Работа с комментариями
  - Управление метками
- **TemplateService**: работа с шаблонами
  - Загрузка шаблонов из файлов
  - CRUD операции с шаблонами
  - Кэширование шаблонов

## Функции API

### Задачи
- Создание задач с шаблонами DoR/DoD
- Получение и обновление задач
- Управление метками задач

### Эпики
- Получение информации об эпике
- Список задач в эпике
- Обновление статуса

### Шаблоны DoR/DoD
- Получение списка шаблонов
- Создание шаблона
- Обновление шаблона
- Удаление шаблона

### Метки
- Получение списка меток
- Информация об использовании метки
- Поиск по меткам

## Эндпоинты API
Роутеры FastAPI с валидацией Pydantic:
- Задачи: CRUD операции
- Эпики: операции чтения и обновления
- Метки: управление пользовательскими метками
- DoR/DoD: работа с шаблонами
- Ссылки: управление веб-ссылками

## Зависимости
```
fastapi==0.109.0
uvicorn==0.27.0
pyyaml==6.0.1
jira==3.5.2
python-dotenv==1.0.0
pydantic==2.5.3
```

## Локальное развертывание

### Установка
1. Клонировать репозиторий:
```bash
git clone https://github.com/your-username/jira-sonnet.git
cd jira-sonnet
```

2. Создать виртуальное окружение:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

### Конфигурация
Создайте файл `.env` в корне проекта:
```
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@domain.com
JIRA_TOKEN=your-api-token
LOG_LEVEL=INFO
```

### Запуск
```bash
cd backend
uvicorn app.main:app --reload
```

## Тестирование

### Структура тестов
```
backend/
├── tests/
│   ├── conftest.py         # Общие фикстуры
│   ├── integration/       # Интеграционные тесты
│   │   └── test_jira.py  # Тесты JIRA API
│   └── test_api/         # Тесты эндпоинтов
       ├── test_tasks.py
       ├── test_epics.py
       ├── test_labels.py
       └── test_templates.py
```

### Запуск тестов
```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Конкретный модуль
pytest tests/test_api/test_templates.py

# С покрытием кода
pytest --cov=app
```

### Переменные окружения для тестов
Создайте файл `.env.test`:
```
JIRA_SERVER=https://test.atlassian.net
JIRA_USERNAME=test@example.com
JIRA_TOKEN=test-token
LOG_LEVEL=DEBUG
```

## Логирование
- Структурированные JSON логи
- Уровни: DEBUG, INFO, WARNING, ERROR
- Логирование запросов и ответов API
- Отслеживание интеграции с JIRA

## Безопасность
- Аутентификация через JIRA API токен
- Валидация входных данных
- Безопасная обработка ошибок
- Ограничение доступа к API
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
│   │       ├── dor_dod.py   # Операции с DoR/DoD
│   │       └── links.py     # Операции с ссылками
│   ├── services/
│   │   └── jira.py         # Функции для работы с JIRA API
│   ├── schemas/            # Pydantic модели
│   │   ├── task.py        
│   │   ├── epic.py
│   │   ├── label.py
│   │   ├── dor_dod.py
│   │   └── link.py
│   └── utils/
       └── helpers.py       # Вспомогательные функции
```

## Основные компоненты

### API Endpoints (v1)
- `/api/v1/tasks/` - управление задачами
- `/api/v1/epics/` - работа с эпиками
- `/api/v1/labels/` - управление метками
- `/api/v1/dor-dod/` - работа с DoR/DoD
- `/api/v1/links/` - управление ссылками

### Модели данных
Pydantic модели для валидации:
- **TaskSchema**: модель задачи
- **EpicSchema**: модель эпика
- **LabelSchema**: модель метки
- **DorDodSchema**: модель шаблона
- **LinkSchema**: модель ссылки

### Хранение данных
- **templates/**: YAML файлы с шаблонами DoR/DoD
- **settings/**: YAML файлы с настройками и метками

### Сервисы
- **JiraService**: работа с JIRA REST API
  - Получение задач и эпиков
  - Обновление задач
  - Работа с комментариями
  - Управление метками

## Функции API
Асинхронные функции для работы с JIRA:
- Получение и обновление задач/эпиков
- Управление комментариями
- Управление метками

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
1. Создать виртуальное окружение:
```bash
python -m venv venv
.\venv\Scripts\activate
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Запустить сервер разработки:
```bash
uvicorn app.main:app --reload
```

## Конфигурация
Создайте файл `.env` в корне проекта:
```
JIRA_URL=https://your-domain.atlassian.net
JIRA_USER=your-email@domain.com
JIRA_TOKEN=your-api-token
```
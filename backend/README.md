# Backend Documentation

## Структура проекта
```
backend/
├── app/
│   ├── main.py              # Основной файл FastAPI приложения
│   ├── core/
│   │   ├── config.py        # Конфигурация приложения и JIRA
│   │   └── logging.py       # Настройки логирования
│   ├── api/
│   │   └── v1/
│   │       ├── tasks.py     # Управление задачами
│   │       ├── epics.py     # Управление эпиками
│   │       ├── labels.py    # Управление метками
│   │       ├── dor_dod.py   # Работа с DoR/DoD
│   │       └── links.py     # Управление ссылками
│   ├── services/
│   │   └── jira.py         # Взаимодействие с JIRA API
│   ├── models/
│   │   ├── task.py         # Модель задачи
│   │   ├── epic.py         # Модель эпика
│   │   ├── label.py        # Модель метки
│   │   ├── dor_dod.py      # Модель DoR/DoD
│   │   └── link.py         # Модель ссылки
│   └── utils/
│       └── helpers.py       # Вспомогательные функции
├── data/
│   ├── templates/          # DoR/DoD шаблоны в YAML
│   └── settings/          # Пользовательские настройки в YAML
└── requirements.txt       # Зависимости проекта
```

## Основные компоненты

### API Endpoints (v1)
- `/api/v1/tasks/` - управление задачами
- `/api/v1/epics/` - работа с эпиками
- `/api/v1/labels/` - управление метками
- `/api/v1/dor-dod/` - работа с DoR/DoD
- `/api/v1/links/` - управление ссылками

### Модели данных
- **Task**: модель задачи с основными полями
- **Epic**: модель эпика и связи с задачами
- **Label**: модель пользовательской метки
- **DorDod**: модель шаблона DoR/DoD
- **Link**: модель веб-ссылки

### Хранение данных
- **templates/**: YAML файлы с шаблонами DoR/DoD
- **settings/**: YAML файлы с настройками и метками

### Сервисы
- **JiraService**: работа с JIRA REST API
  - Получение задач и эпиков
  - Обновление задач
  - Работа с комментариями
  - Управление метками

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
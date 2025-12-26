# Habit Tracker — Backend

Бэкенд-часть SPA-приложения для трекинга полезных привычек по мотивам книги
«Атомные привычки» Джеймса Клира.

Проект реализован в рамках курсовой работы.

## Стек технологий

- Python 3.13
- Django
- Django REST Framework
- JWT (djangorestframework-simplejwt)
- Celery
- Redis
- Telegram Bot API
- PostgreSQL / SQLite (для разработки)
- Poetry
- Pytest

## Функциональность

- Регистрация и авторизация пользователей (JWT)
- CRUD для привычек (доступ только к своим)
- Публичный список привычек (только чтение)
- Валидация бизнес-правил привычек
- Пагинация (5 элементов на страницу)
- Интеграция с Telegram для напоминаний
- Отложенные задачи и периодические напоминания (Celery + Beat)
- Документация API (Swagger)
- Покрытие тестами ≥ 80%
- Flake8 — 100% (кроме миграций)

## Модель привычки

Привычка описывается формулой:

> Я буду [действие] в [время] в [место]

Поддерживаются:
- полезные привычки
- приятные привычки (как вознаграждение)
- периодичность (1–7 дней)
- публичность

## Установка и запуск

```bash
git clone <repo_url>
cd course_work

poetry install
poetry shell
```

### Создайте .env файл:
```
DEBUG=1
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
CELERY_BROKER_URL=redis://localhost:6379/0
TELEGRAM_BOT_TOKEN=your_bot_token
```

### Примените миграции:

```bash
pytest --cov=src
```

### Запуск сервера:

```bash
python src/manage.py runserver
```

### Запуск Celery:

```bash
celery -A config.celery:app worker --pool=solo -l info --workdir=src
celery -A config.celery:app beat -l info --workdir=src
```

### Документация API

Swagger UI:
```bash
http://127.0.0.1:8000/api/docs/
```

### Тесты
```bash
pytest --cov=src
```
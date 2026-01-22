## Course Work — Habit Tracker (DRF + Celery + Telegram)

### Backend для SPA-трекера привычек (по книге «Атомные привычки»).
### Стек: Django + DRF, PostgreSQL, Redis, Celery (worker + beat), Nginx, Docker Compose.

### Сервисы

- web — Django/DRF приложение (Gunicorn)
- db — PostgreSQL
- redis — брокер для Celery
- celery — Celery worker
- celery-beat — Celery beat (планировщик)
- nginx — reverse proxy + раздача статики

### Требования

- Docker + Docker Compose
- (для локальной разработки без Docker) Poetry + Python 3.13

### Переменные окружения

- В репозитории есть шаблон: .env.example
- Создай .env на его основе:

#### Скопировать:

- Linux/macOS:

```cp .env.example .env```


- Windows PowerShell:

```Copy-Item .env.example .env```


- Заполнить значения:
```
SECRET_KEY
POSTGRES_PASSWORD
TELEGRAM_BOT_TOKEN (если нужен Telegram)
```

## Запуск проекта локально (одной командой)

- Создай .env

- Запусти:

```docker compose up -d --build```

#### Проверка:

API через Nginx: 
```http://localhost/```

Админка (если включена): 
```http://localhost/admin/```

#### Остановить:

```docker compose down```

#### Посмотреть логи:

```docker compose logs -f --tail=200 web```

- Миграции и суперпользователь (в Docker)

- Применить миграции (обычно уже выполняется при старте web, но можно вручную):

- docker compose exec web python src/manage.py migrate

### Создать суперпользователя:

```docker compose exec web python src/manage.py createsuperuser```

### Telegram напоминания

#### Логика напоминаний запускается Celery-задачами.

### Проверь:

- celery (worker) запущен

- celery-beat (scheduler) запущен

- Пользователь имеет корректный telegram_chat_id

- TELEGRAM_BOT_TOKEN задан в .env

### Документация API
```
/api/docs/
```

### CI/CD (GitHub Actions)

### Workflow расположен в .github/workflows/ci.yml и делает:

- pytest

- flake8

- проверка сборки Docker образов (docker compose build)

### Автодеплой
```
Деплой выполняется только после merge в develop, потому что job deploy запускается на событии push в ветку develop.
```
###### На pull_request деплой намеренно не выполняется (это безопаснее и соответствует распространённой практике).

## Деплой на сервер (Docker Compose)
#### Требования к серверу

- Ubuntu/Debian (рекомендуется)
- Установлены Docker и Docker Compose Plugin
- Открыт порт 80 (HTTP)
- SSH-доступ по ключу

#### Структура на сервере

- На сервере должен быть каталог, где лежит репозиторий, например:

`````/home/ubuntu/course_work`````

- И внутри него должен быть ```docker-compose.yml```

### Как деплоит GitHub Actions

#### Job deploy подключается по SSH и выполняет:

```git fetch```
```git reset --hard origin/develop```
```docker compose up -d --build```
```docker compose ps```

### Secrets в GitHub

###### В GitHub → Settings → Secrets and variables → Actions должны быть заданы:

###### SSH_HOST — IP/домен сервера

###### SSH_USER — пользователь (например ubuntu)

###### SSH_PRIVATE_KEY — приватный ключ (OpenSSH формат)

###### DEPLOY_PATH — путь до проекта на сервере (например /home/ubuntu/course_work)

## Адрес развернутого сервера

```
http://158.160.216.113/api/docs/
```

### Команды для разработки без Docker

#### Установка зависимостей:
```bash
poetry install
```

#### Миграции:
```bash
poetry run python src/manage.py migrate
```

#### Тесты:
```bash
poetry run pytest
```

#### Линтер:
```bash
poetry run flake8
```
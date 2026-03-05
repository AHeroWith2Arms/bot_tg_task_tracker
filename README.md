## TG Task / Habit Tracker — бэкенд и Telegram‑бот для трекинга привычек

Бэкенд‑приложение на Django/DRF с интеграцией с Telegram‑ботом для трекинга привычек и задач.  
Пользователь формулирует привычку по формуле: «я буду *действие* в *время* в *место*», а сервис напоминает о ней в Telegram в нужный момент.

### Основные возможности

- **Управление пользователями**
  - Регистрация и авторизация по email (JWT‑токены).
  - Хранение `telegram_chat_id` для связи аккаунта с Telegram.

- **Привычки и напоминания**
  - Создание, редактирование и удаление привычек.
  - Поля: место, время, действие, периодичность, тип привычки (приятная/обычная), публичность.
  - Гибкая бизнес‑валидация (ограничения по времени выполнения, периодичности, наградам и связанным привычкам).
  - Публичные привычки, видимые другим пользователям.

- **Интеграция с Telegram**
  - Фоновые задачи Celery, которые ищут «наступившие» по времени привычки.
  - Отправка напоминаний пользователям в Telegram через Telegram Bot API.

- **API**
  - REST API на Django REST Framework.
  - JWT‑аутентификация.
  - Пагинация, базовые права доступа и автогенерируемая OpenAPI‑схема (drf-spectacular).

Более детальное описание технологий и архитектуры см. в файле `FEATURES.md`.

---

## Технологический стек

- **Python 3.11+**
- **Django 5**
- **Django REST Framework**
- **PostgreSQL**
- **Celery + Redis** (фоновые задачи и планировщик)
- **Telegram Bot API** (через `requests`)
- **JWT‑аутентификация** (`djangorestframework-simplejwt`)
- **drf-spectacular** для OpenAPI‑схемы
- **django-environ** для конфигурации
- **pytest / pytest-django / coverage / flake8 / black** для тестов и качества кода

---

## Структура проекта

- `config/` — настройки Django, `urls.py`, конфигурация Celery.
- `users/` — кастомная модель пользователя, сериализаторы и API.
- `habits/` — модель привычек, бизнес‑валидация, сериализаторы, представления и роуты.
- `telegram_bot/` — задачи Celery для рассылки напоминаний в Telegram.
- `tests/` — тесты для пользователей и привычек.
- `pyproject.toml` — зависимости и настройки инструментов разработки.

---

## Требования

- Python `>= 3.11`
- PostgreSQL (локальный или в контейнере)
- Redis (для брокера/бэкенда Celery)

---

## Переменные окружения

Проект использует `.env` файл в корне (рядом с `manage.py`). Пример минимального набора:

```env
DEBUG=True
SECRET_KEY=your-secret-key

POSTGRES_DB=tg_task_tracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## Установка и запуск (локально)

1. **Клонировать репозиторий**

   ```bash
   git clone <url_репозитория>
   cd bot_tg_task_tracker
   ```

2. **Создать и активировать виртуальное окружение**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/MacOS
   ```

3. **Установить зависимости**

   ```bash
   pip install -U pip
   pip install .
   ```

   При использовании Poetry:

   ```bash
   poetry install
   ```

4. **Подготовить базу данных**

   Убедитесь, что PostgreSQL запущен и параметры в `.env` корректны.

   ```bash
   python manage.py migrate
   ```

5. **Создать суперпользователя (по желанию)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Запустить приложение**

   ```bash
   python manage.py runserver
   ```

7. **Запустить Celery‑воркер и планировщик**

   В отдельных терминалах:

   ```bash
   celery -A config worker -l info
   celery -A config beat -l info
   ```

   Либо запустить только `worker`, если планирование задач вынесено во внешнюю систему (например, crontab, systemd timer и т.п.).

---

## Работа Telegram‑напоминаний

- В приложении `habits` пользователь создаёт привычку, указывая:
  - место (`place`);
  - время (`time`);
  - действие (`action`);
  - периодичность (`periodicity`) и прочие поля.
- В модели `User` хранится `telegram_chat_id`, который должен быть получен ботом в ходе диалога с пользователем.
- Периодическая задача Celery `send_due_habits_reminders`:
  - находит все привычки, время которых «наступило» сейчас;
  - группирует их по пользователям;
  - отправляет сообщения в Telegram через Bot API на соответствующие `telegram_chat_id`.

---

## Тестирование и качество кода

- Запуск тестов:

  ```bash
  pytest
  ```

- Подсчёт покрытия:

  ```bash
  coverage run -m pytest
  coverage report
  ```

- Проверка линтера и автоформатирование:

  ```bash
  flake8
  black .
  ```

---

## Как использовать этот проект

- **В качестве учебного проекта**: показать работу с Django/DRF, Celery, JWT и интеграцией с внешним сервисом (Telegram).
- **Как основу для продакшен‑сервиса**: доработать UI, добавить полноценного Telegram‑бота (диалоги, команды), расширить модель привычек.
- **Как демонстрацию технологичного бэкенда**: см. файл `FEATURES.md` для презентации ключевых особенностей.


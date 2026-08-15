# Habit Tracker

Backend-приложение для трекера полезных привычек.

Проект разработан на Django и Django REST Framework. Пользователь может создавать и управлять привычками, а система автоматически отправляет напоминания о выполнении привычек через Telegram.

## Возможности

- регистрация и авторизация пользователей;
- JWT-аутентификация;
- создание, просмотр, изменение и удаление привычек;
- разделение привычек на публичные и личные;
- приятные привычки и связанные привычки;
- валидация правил создания привычек;
- пагинация списка привычек;
- CORS;
- интеграция с Telegram;
- автоматические напоминания;
- фоновые задачи Celery;
- периодические задачи Celery Beat;
- Redis в качестве брокера сообщений;
- тестирование API;
- покрытие проекта тестами более 80%.

## Технологии

- Python
- Django
- Django REST Framework
- Simple JWT
- Celery
- django-celery-beat
- Redis
- SQLite
- Telegram Bot API
- drf-spectacular
- Coverage
- Flake8

## Установка

Клонируйте репозиторий и перейдите в папку проекта.

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте его в Windows:

```bash
.venv\Scripts\activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте файл `.env` на основе `.env.template` и заполните необходимые переменные окружения.

Выполните миграции:

```bash
python manage.py migrate
```

Запустите сервер:

```bash
python manage.py runserver
```

## Celery

Для работы фоновых задач должен быть запущен Redis.

Запуск Celery Worker в Windows:

```bash
celery -A config worker -l info -P solo
```

В отдельном терминале запустите Celery Beat:

```bash
celery -A config beat -l info
```

## Telegram

Для получения уведомлений необходимо:

1. Создать Telegram-бота через BotFather.
2. Добавить токен бота в `.env`.
3. Запустить бота командой `/start`.
4. Указать Telegram chat ID пользователя.

После этого система сможет отправлять напоминания о привычках через Telegram.

## API документация

После запуска сервера документация API доступна по адресу:

```text
http://127.0.0.1:8000/api/docs/
```

## Тестирование

Запуск всех тестов:

```bash
python manage.py test
```

Проверка покрытия:

```bash
coverage run manage.py test
coverage report
```

Текущее покрытие проекта тестами — 96%.

## Проверка качества кода

```bash
flake8 config habits users --exclude=migrations --max-line-length=88
```

## Переменные окружения

Пример необходимых переменных находится в файле `.env.template`.

Настоящие секретные данные и токен Telegram-бота не должны добавляться в репозиторий.

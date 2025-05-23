# Booking-Flight
Сервис для бронирования мест на авиарейсы.

> [!IMPORTANT]
> Проект в стадии разработки.

Задуман для регистрации брони позователями на места на рейсы местной авиакомпании через сайт или телеграм, а также для администратора сервиса для ведения записей бронирования, вылетов рейсов, стоимости билетов и тд. 

## Технологии:
  - FastAPI
  - SQLAlchemy
  - Pydantic
  - Alembic
## TODO
  - [x] модели БД
  - [x] Схемы Pydantic
  - [X] CRUD
  - [x] API (в стадии наполнения)
  - [ ] Telegram-bot
  - [ ] Docker
## Установка
- Клонировать репозиторий и перейти в него в командной строке:

    ```bash
    git clone git@github.com:corbuncul/booking_flight.git
    ```

    ```bash
    cd booking_flight
    ```

- Cоздать и активировать виртуальное окружение:

    При разработке использовалась версия python 3.12

    ```bash
    python3 -m venv venv
    ```

    * Если у вас Linux/macOS

        ```bash
        source venv/bin/activate
        ```

    * Если у вас windows

        ```bash
        source venv/scripts/activate
        ```

- Установить зависимости из файла requirements.txt:

    ```bash
    python3 -m pip install --upgrade pip
    ```

    ```bash
    pip install -r requirements.txt
    ```
- Создать файл ".env" и прописать константы:

    ```ini
    AP_TITLE=Ваше название приложения
    AP_DESCRIPTION=Ваше краткое описание приложения
    AP_SECRET=Ваш секртный ключ (любая случайная строка)
    DB_DATABASE_URL=Ваше подключение к базе данных (например: sqlite+aiosqlite:///./fastapi.db)
    SU_SUPERUSER_EMAIL=Ваш email для первого суперпользователя. Если указан, при первом запуске будет создан суперпользователь.
    SU_SUPERUSER_PASSWORD=Ваш пароль суперпользователя
    ```
- Применить миграции:

    ```bash
    alembic upgrade head
    ```
## Запуск проекта:

```bash
uvicorn app.main:app
```

Проект будет доступен по адресу http://localhost:8000/

Подергать ручки http://localhost:8000/docs/

# Построение защищённого API для работы с большой языковой моделью.
Выполнил: Хилалов Муслим\
Группа: М25-555

## Описание возможностей

- регистрация пользователей;
- аутентификация пользователей с использованием access JWT-токена;
- получение профиля текущего пользователя;
- написание сообщений к LLM (с контекстом в виде истории и системных инструкций);
- отображение истории сообщений;
- удаление истории сообщений.

## Инструкция к сборке и запуску приложения

1. Клонируйте репозиторий командой `git clone https://github.com/javachka11/llm-p`;
2. Перейдите в директорию проекта командой `cd llm-p`;
3. Скопируйте `.env.example` в `.env` командой `cp .env.example .env`;
4. Отредактируйте файл `.env` (добавьте API-ключ OpenRouter, по желанию поменяйте другие поля);
5. Установите библиотеку `uv` в случае её отсутствия командой `pip install uv`;
6. Синхронизируйтесь с виртуальным окружением проекта командой `uv sync`;
7. Запустите приложение командой `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`;
8. Готово! Можете проверить статус приложения, перейдя по ссылке [http://0.0.0.0:8000/health](http://0.0.0.0:8000/health).

## API Документация

Swagger UI: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

## API Эндпоинты

|Эндпоинт|Описание|
|:-|:-|
|`GET /health`|получить статус приложения|
|`POST /auth/register`|зарегистрировать нового пользователя|
|`POST /auth/login`|залогиниться (с получением JWT-токена)
|`GET /auth/me`|получить профиль текущего пользователя|
|`POST /chat`|отправить сообщение в LLM|
|`GET /chat/history`|получить историю чата|
|`DELETE /chat/history`|удалить историю чата|

## Скриншоты работы эндпоинтов

### Swagger UI
![Swagger Documentation](docs/screenshots/swagger.png)

### Health-check
![Health](docs/screenshots/health.png)

### Регистрация пользователя
![Register](docs/screenshots/register.png)

### Регистрация пользователя (email уже существует)
![Register](docs/screenshots/conflict.png)

### Логин и получение JWT
![Login](docs/screenshots/login_1.png)
![Login](docs/screenshots/login_2.png)

### Логин и получение JWT (пользователя не существует)
![Login](docs/screenshots/noauth_1.png)
![Login](docs/screenshots/noauth_2.png)

### Логин и получение JWT (неверный пароль)
![Login](docs/screenshots/noauth_3.png)
![Login](docs/screenshots/noauth_4.png)

### Авторизация через Swagger
![Autentification](docs/screenshots/auth_1.png)
![Autentification](docs/screenshots/auth_2.png)

### Вызов POST /chat
![Chat](docs/screenshots/chat_1.png)
![Chat](docs/screenshots/chat_2.png)

### Получение истории через GET /chat/history
![History](docs/screenshots/chat_history.png)

### Удаление истории через DELETE /chat/history
![Delete](docs/screenshots/delete.png)
![Delete](docs/screenshots/deleted_chat_history.png)

### Получение профиля текущего пользователя (JWT действителен)
![ActiveJWT](docs/screenshots/profile_jwt.png)

### Получение профиля текущего пользователя (JWT истёк)
![ExpiredJWT](docs/screenshots/profile_nojwt.png)
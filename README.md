# T-Ledger

Сервис для учета инвестиционных портфелей и анализа активов с интеграцией в T-Invest API.
Основной интерфейс взаимодействия — Telegram-бот.

---

## Требования перед запуском

Проект использует внешние API, поэтому перед запуском необходимо получить токены.
Без указанных токенов приложение работать не будет.

### T-Invest API

Получить API токен можно в официальной документации:
[https://developer.tbank.ru/invest/intro/intro/token](https://developer.tbank.ru/invest/intro/intro/token)

### Telegram Bot

Создать бота и получить токен можно через BotFather:
[https://core.telegram.org/bots/features#botfather](https://core.telegram.org/bots/features#botfather)

---

## Конфигурация (.env)

Файл `.env` обязателен для запуска приложения.

Вставьте ранее полученные токены:

```dotenv
TGBOT__TOKEN=your_telegram_bot_token
TGBOT__ALLOWED_USER_IDS_STR=111111111|222222222

TBANK__TOKEN=your_tbank_access_token
TBANK__BASE_URL=https://invest-public-api.tbank.ru/rest
```

### Ограничение доступа к боту

`TGBOT__ALLOWED_USER_IDS_STR` — список Telegram user ID, которым разрешён доступ к боту.

Формат: строка с разделителем `|`.

```dotenv
TGBOT__ALLOWED_USER_IDS_STR=111111111|222222222|333333333
```

Если пользователь отсутствует в списке — доступ будет отклонён.

### Как узнать свой Telegram ID

Напишите боту `@userinfobot` — он вернёт ваш `user_id`.

---

## Быстрый старт

```bash
git clone https://github.com/noname-224/t-ledger.git
cd t-ledger

cp .env.example .env
# заполните .env (укажите токены)

docker compose up --build
```

---

## О проекте

T-Ledger — учебный backend-сервис, демонстрирующий работу с инвестиционными данными и внешними API.

### Возможности

- управление инвестиционным портфелем
- расчет распределения активов
- анализ рисков облигаций
- интеграция с T-Invest API
- Telegram-интерфейс для взаимодействия

---

## Архитектура

Проект построен по принципам слоистой архитектуры:

```
presentation → application → domain ← infrastructure
```

### Слои:

* **presentation** — Telegram-интерфейс
* **application** — бизнес-логика (use-cases)
* **domain** — модели, интерфейсы, value objects
* **infrastructure** — интеграции (API, репозитории)

---

## Технологии

* Python 3.13
* SQLAlchemy (async)
* PostgreSQL
* Alembic
* Pydantic
* PyJWT
* Docker / Docker Compose
* Poetry

---

## Тестирвоание

Установить зависимости и создать виртуальное окружение:

```bash
poetry install
```

Активировать виртуальное окружение:
```bash
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```

Запустить тесты:

```bash
pytest -s -v
```

---

## Миграции

Создание миграции:

```bash
alembic revision --autogenerate -m "message"
```

Применение:

```bash
alembic upgrade head
```

Откат:

```bash
alembic downgrade -1
```

---

## Структура проекта

```
t_ledger/

  application/      # бизнес-логика (use-cases)
  domain/           # модели и интерфейсы
  infra/            # интеграции и репозитории
  presentation/     # Telegram слой

  config.py         # конфигурация
  containers.py     # DI контейнер
  main.py           # точка входа

tests/              # тесты
```

---

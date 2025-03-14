# WB Price Bot

## Описание проекта
Этот бот отслеживает изменения цен на товары и уведомляет пользователей о них. Используется для мониторинга стоимости товаров на Wildberries.


## Используемые технологии
- **Python**
- **SQLite** (в качестве БД)
- **Aiogram** (для работы с Telegram-ботом)
- **SQLAlchemy** (ORM для работы с БД)
- **Alembic** (для миграций БД)
- **aiohttp** (для получения данных с Wildberries)
- **Docker** (для контейнеризации)

## 🔹 Доступные команды

### 📌 Основные команды:
- **`/start`** — начало работы и регистрация пользователя.
- **`/help`** — показывает доступные команды и инструкцию пользования.
- **`/menu`** — открывает главное меню.
- **`/products`** — список отслеживаемых товаров.

### 🛍 Добавление товаров
- Чтобы добавить товар в список отслеживаемых, просто отправьте **артикул** или **ссылку на товар** боту.
- Максимальное количество товаров на одного пользователя — **5**.

### 🔧 Команды администратора:
- **`/list`** — показывает список пользователей, которым разрешено пользоваться ботом.
- **`/add (username)`** — разрешает пользователю пользоваться ботом.
- **`/remove (username)`** — удаляет пользователя из списка разрешенных.

📌 **Бот создан для индивидуального использования**. Только пользователи, добавленные администратором, могут им пользоваться.


## Запуск программы

### 🔹 Обычный запуск
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Создайте файл .env (можно использовать .env-example в качестве примера) и укажите необходимые параметры.
   
3. Запустите бота:
   ```bash
   python main.py
   ```

### 🐳 Запуск через Docker
1. Соберите образ:
   ```bash
   docker build -t wb_price_bot .
   ```
3. Запустите контейнер:
   ```bash
   docker run --env-file .env wb_price_bot
   ```
Для запуска через docker-compose:
```bash
docker-compose up --build -d
```


   

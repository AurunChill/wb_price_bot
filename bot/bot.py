import logging
from logging.handlers import RotatingFileHandler
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from config import settings

# Инициализация логгера
logger = logging.getLogger(__name__)

# Конфигурация обработчиков
handlers = [
    RotatingFileHandler(
        filename=settings.logging.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=3,
        encoding="utf-8",
    ),
    logging.StreamHandler(),
]

# Базовая настройка логирования
logging.basicConfig(
    level=settings.logging.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=handlers,
)


class CustomBot(Bot):
    async def setup(self) -> None:
        logger.info("Starting bot initialization...")
        await super().setup()

    async def on_startup(self, dispatcher: Dispatcher) -> None:
        logger.info("Bot started successfully ✅")

    async def on_shutdown(self, dispatcher: Dispatcher) -> None:
        logger.warning("Bot shutdown initiated ⚠️")
        await super().on_shutdown(dispatcher)


# Инициализация бота
bot = CustomBot(
    token=settings.bot.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")
)
dispatcher = Dispatcher(bot=bot)

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.bot import bot, dispatcher
from bot.handlers import routers
from bot.handlers.background import check_prices
from bot.data.database import create_tables, run_migrations
from bot.middleware import CheckUserMiddleware
from config import settings


async def start_bot():
    dispatcher.include_routers(*routers)
    dispatcher.message.middleware.register(CheckUserMiddleware())
    dispatcher.callback_query.middleware.register(CheckUserMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, allowed_updates=["message", "callback_query"])


async def main():
    await create_tables()
    await run_migrations()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_prices, "interval", minutes=settings.bot.PRICE_INTERVAL)
    scheduler.start()

    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())

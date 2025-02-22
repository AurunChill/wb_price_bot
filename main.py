import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.bot import bot, dispatcher
from bot.handlers import routers
from bot.handlers.background import check_prices
from bot.data.database import create_tables


async def start_bot():
    dispatcher.include_routers(*routers)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, allowed_updates=["message", "callback_query"])


async def main():
    create_tables()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_prices, "interval", minutes=5)
    scheduler.start()

    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())

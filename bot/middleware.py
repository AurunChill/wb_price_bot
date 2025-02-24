from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from config import settings

class CheckUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message):
            username = event.from_user.username
            user_id = str(event.from_user.id)
            if username.lower() not in settings.bot.ALLOWED_USERS and user_id not in settings.bot.ALLOWED_USERS:
                await event.answer("<b>Вы не можете пользоваться ботом!</b> 😊")
                return
        return await handler(event, data)
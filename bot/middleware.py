from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from bot.data.services.allowed_users_service import AllowedUserService
from bot.data.database import async_session
from config import settings


class CheckUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, (types.Message, types.CallbackQuery)):
            user = event.from_user
            
            admins = [admin.lower() for admin in settings.bot.ADMINS]
            if str(user.id) not in admins and user.username.lower() not in admins:
                async with async_session() as session:
                    service = AllowedUserService(session)
                    if not await service.is_allowed(user.id):
                        await event.answer("<b>Доступ запрещён!</b> 🔒")
                        return

        return await handler(event, data)
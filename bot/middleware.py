from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from bot.data.services.allowed_users_service import AllowedUserService
from bot.data.services.user_service import UserService
from bot.data.database import async_session
from config import settings


class CheckUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, (types.Message, types.CallbackQuery)):
            user = event.from_user
            
            admins = [admin.lower() for admin in settings.bot.ADMINS]
            if str(user.id) not in admins and user.username.lower() not in admins:
                service = AllowedUserService(async_session)
                user_id = user.id
                username = user.username.lower()
                if not await service.is_allowed_by_id(user_id) and not await service.is_allowed_by_username(username):
                    await event.answer("<b>Доступ запрещён!</b> 🔒")
                    return

        return await handler(event, data)


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Пропускаем команду /start и её вариации
        if event.text and event.text.strip().startswith('/start'):
            return await handler(event, data)

        user_service = UserService(async_session)
        user = await user_service.get_by_id(event.from_user.id)
            
        if not user:
            await event.answer(
                "🚫 Для работы с ботом необходимо начать с команды /start",
            )
            return

        return await handler(event, data)
    

def register_middlewares(dp: Dispatcher):
    dp.message.middleware.register(CheckUserMiddleware())
    dp.callback_query.middleware.register(CheckUserMiddleware())
    dp.message.middleware.register(RegistrationMiddleware())
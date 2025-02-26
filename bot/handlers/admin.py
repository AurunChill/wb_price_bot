from aiogram import Router, F
from aiogram.types import Message
import re
from bot.data.database import async_session
from bot.data.services.allowed_users_service import AllowedUserService
from bot.data.services.user_service import UserService
from bot.data.services.product_service import ProductService    
from config import settings

router = Router()


def parse_username(identifier: str) -> str:
    """Извлекает username из любых форматов"""
    identifier = identifier.split()[0]
    match = re.search(r"(?:t\.me/|@)?([\w_]+)", identifier)
    return match.group(1).lower() if match else identifier.lstrip("@").lower()


def is_admin(user):
    admins = [admin.lower() for admin in settings.bot.ADMINS]
    return user.username.lower() in admins or user.id in admins


@router.message(F.text.startswith("/add"))
async def add_user(message: Message):
    if not is_admin(message.from_user):
        return

    try:
        # Разделяем сообщение на части и берем первый аргумент после /add
        parts = message.text.split()
        if len(parts) < 2:
            raise ValueError("Не указан идентификатор")

        identifier = " ".join(parts[1:])  # Объединяем все аргументы после /add
        identifier = identifier.strip()

        allowed_service = AllowedUserService(async_session)

        # Обработка user_id
        if identifier.isdigit():
            user_id = int(identifier)
            if await allowed_service.is_allowed_by_id(user_id):
                await message.answer("ℹ️ Пользователь уже имеет доступ")
                return

            await allowed_service.add_user(user_id)
            await message.answer(f"✅ Пользователь [ID: {user_id}] добавлен")

        # Обработка username/ссылки
        else:
            username = parse_username(identifier)

            if await allowed_service.is_allowed_by_username(username):
                await message.answer("ℹ️ Пользователь уже имеет доступ")
                return

            await allowed_service.add_user(username=username)
            await message.answer(f"✅ Пользователь @{username} добавлен")

    except Exception as e:
        print(e)
        await message.answer(
            "❌ Некорректный формат. Примеры:\n"
            "/add @username\n"
            "/add 123456\n"
            "/add https://t.me/username"
        )


@router.message(F.text.startswith("/remove"))
async def remove_user(message: Message):
    if not is_admin(message.from_user):
        return

    try:
        _, identifier = message.text.split(maxsplit=1)
        identifier = identifier.strip()

        allowed_service = AllowedUserService(async_session)
        user_service = UserService(async_session)
        product_service = ProductService(async_session)

        # Удаление из allowed_users
        if identifier.isdigit():
            user_id = int(identifier)
            user = await user_service.get_by_id(user_id)
            success = await allowed_service.remove_user_by_id(user_id)
        else:
            username = parse_username(identifier)
            user = await user_service.get_by_username(username)
            success = await allowed_service.remove_user_by_username(username)

        # Если пользователь найден в основной базе
        if user:
            # Удаляем все связанные объекты (пример для Product)
            await product_service.delete_all_by_user_id(user.user_id)


        response = "✅ Удалено (включая связанные данные)" if success else "❌ Пользователь не найден"
        await message.answer(response)

    except Exception as e:
        print(e)
        await message.answer(
            "❌ Ошибка формата. Используйте:\n"
            "/remove @username\n/remove 123456\n/remove https://t.me/username"
        )


@router.message(F.text == "/list")
async def list_allowed_users(message: Message):
    if not is_admin(message.from_user):
        return

    allowed_service = AllowedUserService(async_session)
    users = await allowed_service.get_all()

    if not users:
        await message.answer("📭 Список разрешенных пользователей пуст")
        return

    user_list = []
    for idx, user in enumerate(users, 1):
        line = f"{idx}. "
        if user.user_id:
            line += f"🆔 <code>{user.user_id}</code>"
        if user.username:
            line += (
                f" │ 👤 @{user.username}"
                if user.user_id
                else f"👤 @{user.username}"
            )
        user_list.append(line)

    response = (
        "📋 <b>Список разрешенных пользователей:</b>\n\n"
        + "\n".join(user_list)
        + "\n\n<i>Используйте /add или /remove для управления</i>"
    )

    await message.answer(response)

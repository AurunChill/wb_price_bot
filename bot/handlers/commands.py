from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.data.database import async_session
from bot.data.services.user_service import UserService
from bot.data.models.user import User

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    user = await UserService(async_session).get_by_id(message.chat.id)
    if not user:
        new_user = User(
            user_id=message.chat.id,
            username=message.from_user.full_name,
            link=f"t.me/{message.from_user.username}",
        )
        await UserService(async_session).create(new_user)

    await message.answer(
        "<b>🛍 Добро пожаловать в PriceTrackerBot!</b>\n\n"
        "Я помогу вам отслеживать цены на товары Wildberries и экономить деньги!\n\n"
        "🌟 <i>Основные возможности:</i>\n"
        "✅ Автоматическое отслеживание изменений цен\n"
        "📊 История минимальных и максимальных цен\n"
        "🔔 Мгновенные уведомления о скидках\n"
        "📦 Лёгкое управление списком товаров\n\n"
        "📌 <i>Как начать:</i>\n"
        "1. Отправьте мне артикул товара\n"
        "2. Или поделитесь ссылкой на товар\n"
        "3. Добавляйте несколько товаров за раз!\n\n"
        "Пример: <code>123456789, 987654321</code>\n\n"
        "💡 Используйте кнопки ниже или команды:\n"
        "/menu - Главное меню\n"
        "/help - Подробная инструкция",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📚 Список товаров", 
                        callback_data="products"
                    ),
                    InlineKeyboardButton(
                        text="❓ Помощь", 
                        callback_data="help"
                    )
                ]
            ]
        ),
    )


@router.message(F.text == "/menu")
async def menu(message: Message):
    await message.answer(
        "📌 <b>Главное меню</b>:\n\n"
        "• /products - Отслеживаемые товары\n"
        "• /help - Подробная инструкция",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="❓ Помощь", callback_data="help"),
                    InlineKeyboardButton(text="📚 Товары", callback_data="products")
                ]
            ]
        )
    )


@router.callback_query(F.data == "menu")
async def main_menu(callback: CallbackQuery):
    await menu(message=callback.message)
    await callback.answer()


@router.message(F.text == "/help")
async def help(message: Message):
    await message.answer(
        "📝 <b>Список команд:</b>\n"
        "<i>/start</i> - Начало работы\n"
        "<i>/menu</i> - Главное меню\n"
        "<i>/products</i> - Ваши товары\n"
        "<i>/add {имя пользователя или его id}</i> - Добавить пользователя\n"
        "<i>/remove {имя пользователя или его id}</i> - Удалить пользователя\n"
        "<i>/list</i> - Список пользователей\n\n"
        "Отправьте <b>артикул</b> или <b>ссылку</b> на товар. Если хотите добавить несколько товаров, то указывайте их через <b>запятую</b>!\n\n"
        "<code>51523547</code>\n\nИЛИ\n\n"
        "<code>https://www.wildberries.ru/catalog/51523547/detail.aspx</code>\n\nИЛИ\n\n"
        "<code>51523547, 319796142</code>\n\nИЛИ\n\n"
        "<code>https://www.wildberries.ru/catalog/51523547/detail.aspx, https://www.wildberries.ru/catalog/319796142/detail.aspx</code>",
    )


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    await help(message=callback.message)
    await callback.answer()
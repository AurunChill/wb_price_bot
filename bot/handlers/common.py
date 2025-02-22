import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.data.database import db
from bot.data.models.product import Product
from bot.data.services.product_service import ProductService
from parser.wildberries import AsyncWildberriesParser

router = Router()


@router.message(F.text)
async def handle_products(message: Message):
    articles = list(set(re.findall(r"\d+", message.text)))
    user_id = message.chat.id
    product_service = ProductService(db)

    added_products = []
    existing_articles = []

    wait_msg = await message.answer("⌛ Поиск товаров...\n\nПожалуйста, подождите...")
    async with AsyncWildberriesParser() as parser:
        for article in articles:
            # Проверяем существование товара
            if product_service.get_by_article_and_user(article, user_id):
                existing_articles.append(article)
                continue

            # Получаем данные
            product_info = await parser.get_product_info(article)
            if not product_info:
                continue

            # Создаем продукт
            product = product_service.create(Product(user_id=user_id, **product_info))
            added_products.append(product)

    # Формируем ответ
    response_messages = []

    await wait_msg.delete()
    if added_products:
        builder = InlineKeyboardBuilder()
        for product in added_products:
            builder.button(
                text=f"📦 {product.name}", callback_data=f"product_{product.id}"
            )
        builder.adjust(2)

        response_messages.append(
            await message.answer(
                f"✅ Успешно добавлено товаров: {len(added_products)} шт.",
                reply_markup=builder.as_markup(),
            )
        )

    if existing_articles:
        articles_list = ", ".join(existing_articles)
        response_messages.append(
            await message.answer(
                f"ℹ️ Эти товары уже были добавлены ранее:\n<code>{articles_list}</code>"
            )
        )

    if not added_products and not existing_articles:
        await message.answer("❌ Не удалось найти ни одного товара")

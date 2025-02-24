from typing import List, Union
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.data.models.product import Product
from bot.data.database import async_session
from bot.data.services.product_service import ProductService

router = Router()


@router.message(F.text == "/products")
async def show_products(message: Message):
    """Показывает список товаров с кнопкой обновления"""
    products = await ProductService(async_session).get_by_user(message.chat.id)
    await _send_products_message(message, products)


@router.callback_query(F.data == "refresh_products")
async def refresh_products(callback: CallbackQuery):
    """Обработчик обновления списка товаров"""
    products = await ProductService(async_session).get_by_user(callback.message.chat.id)
    await callback.message.edit_reply_markup(reply_markup=None)  # Удаляем старые кнопки
    await _send_products_message(callback.message, products, is_edit=True)
    await callback.answer("♻️ Список обновлен")


async def _send_products_message(
    message: Union[Message, CallbackQuery],
    products: List[Product],
    is_edit: bool = False,
):
    """Универсальная функция отправки/редактирования сообщения"""
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки товаров
    for product in products:
        builder.button(text=f"📦 {product.name}", callback_data=f"product_{product.id}")

    # Добавляем кнопку обновления
    builder.button(text="🔄 Обновить", callback_data="refresh_products")

    builder.adjust(2, 1)  # 2 колонки для товаров, 1 для кнопки обновления

    text = (
        f"📦 Ваши товары ({len(products)} шт.):"
        if products
        else "😢 Товаров не найдено"
    )

    if is_edit:
        await message.edit_text(text, reply_markup=builder.as_markup())
    else:
        await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(F.data == "products")
async def show_products_callback(callback: CallbackQuery):
    await show_products(message=callback.message)
    await callback.answer()


@router.callback_query(F.data.startswith("product_"))
async def product_detail(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await ProductService(async_session).get_by_id(product_id)

    if not product:
        return await callback.answer("😢 Товар не найден")

    # Формируем информацию об изменении цены
    price_info = ""
    if product.prev_price and product.prev_price != product.current_price:
        difference = product.current_price - product.prev_price
        percent = abs(difference / product.prev_price * 100)
        trend = "📈 Выросла" if difference > 0 else "📉 Упала"
        price_info = (
            f"{trend} с <s>{product.prev_price} руб.</s> "
            f"до <b>{product.current_price} руб.</b>\n"
            f"<b>Разница:</b> {abs(difference):.2f} руб. ({percent:.2f}%)\n"
            f"<b>Обновлено:</b> {product.prev_price_date}\n\n"
        )
    else:
        price_info = "🔄 Цена не менялась\n\n"

    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Удалить", callback_data=f"delete_{product.id}")
    builder.button(text="↩️ К товарам", callback_data="products")
    builder.adjust(2)

    info_text = (
        f"📊 <b>Информация о товаре:</b>\n"
        f"{price_info}"
        f"• Артикул: {product.article}\n"
        f"• Название: <a href='{product.link}'>{product.name}</a>\n"
        f"• Остаток: {product.stock} шт.\n"
        f"• Цена: {product.current_price} руб.\n"
        f"• Минимум: {product.min_price} ({product.min_price_date})\n"
        f"• Максимум: {product.max_price} ({product.max_price_date})"
    )

    await callback.message.answer_photo(
        photo=product.image_url, caption=info_text, reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    await ProductService(async_session).delete(product_id)
    await callback.message.delete()
    await callback.answer("🗑 Товар успешно удален!")
    await refresh_products(callback)

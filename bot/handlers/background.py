from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot import bot
from bot.data.database import async_session
from bot.data.services.product_service import ProductService
from parser.wildberries import AsyncWildberriesParser


async def check_prices():
    products = await ProductService(async_session).get_all()
    
    async with AsyncWildberriesParser() as parser:
        for product in products:
            try:
                current_info = await parser.get_product_info(product.article)
                if not current_info:
                    continue
                
                # Проверяем изменение цены
                if current_info["current_price"] != product.current_price:
                    # Формируем сообщение как в product_detail
                    difference = current_info["current_price"] - product.current_price
                    percent = abs(difference / product.current_price * 100)
                    trend = "📈 Выросла" if difference > 0 else "📉 Упала"
                    
                    # Обновляем мин/макс цены
                    new_min_price = product.min_price
                    new_min_date = product.min_price_date
                    new_max_price = product.max_price
                    new_max_date = product.max_price_date
                    
                    if current_info["current_price"] < product.min_price:
                        new_min_price = current_info["current_price"]
                        new_min_date = datetime.now().strftime("%d-%m-%Y %H:%M")
                        
                    if current_info["current_price"] > product.max_price:
                        new_max_price = current_info["current_price"]
                        new_max_date = datetime.now().strftime("%d-%m-%Y %H:%M")

                    # Формируем сообщение
                    caption = (
                        f"💰 <b>ИЗМЕНЕНИЕ ЦЕНЫ</b>\n\n"
                        f"{trend} с <s>{product.current_price} руб.</s> "
                        f"до <b>{current_info['current_price']} руб.</b>\n"
                        f"Разница: {abs(difference):.2f} руб. ({percent:.2f}%)\n\n"
                        f"📊 <b>Текущая информация:</b>\n"
                        f"• Название: <a href='{product.link}'>{product.name}</a>\n"
                        f"• Артикул: {product.article}\n"
                        f"• Текущая цена: {current_info['current_price']} руб.\n"
                        f"• Остаток: {current_info['stock']} шт.\n"
                        f"• Мин. цена: {new_min_price} ({new_min_date})\n"
                        f"• Макс. цена: {new_max_price} ({new_max_date})"
                    )

                    # Отправляем карточку с фото
                    await bot.send_photo(
                        chat_id=product.user_id,
                        photo=product.image_url,
                        caption=caption,
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(
                                    text="📜 Список товаров", 
                                    callback_data="products"
                                )]
                            ]
                        )
                    )

                    # Обновляем данные в БД
                    await ProductService(async_session).update(
                        product.id,
                        current_price=current_info["current_price"],
                        prev_price=product.current_price,
                        prev_price_date=datetime.now().strftime("%d-%m-%Y %H:%M"),
                        stock=current_info["stock"],
                        image_url=current_info["image_url"],
                        min_price=new_min_price,
                        min_price_date=new_min_date,
                        max_price=new_max_price,
                        max_price_date=new_max_date
                    )
                    
            except Exception as e:
                print(f"Ошибка при проверке цены для товара {product.article}: {str(e)}")

                
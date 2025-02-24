from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.data.models.product import Product

class ProductService:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def create(self, product: Product) -> Product:
        async with self.session_factory() as db: 
            try:
                db.add(product)
                await db.commit()
                await db.refresh(product)
                return product
            except Exception:
                await db.rollback()
                raise

    async def delete(self, product_id: int) -> None:
        async with self.session_factory() as db:
            try:
                product = await db.get(Product, product_id)
                if product:
                    await db.delete(product)
                    await db.commit()
            except Exception:
                await db.rollback()
                raise

    async def update(self, product_id: int, **kwargs) -> Optional[Product]:
        async with self.session_factory() as db:
            try:
                product = await db.get(Product, product_id)
                if product:
                    for key, value in kwargs.items():
                        if hasattr(product, key):
                            setattr(product, key, value)
                    await db.commit()
                    await db.refresh(product)
                return product
            except Exception:
                await db.rollback()
                raise

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        async with self.session_factory() as db:
            return await db.get(Product, product_id)

    async def get_all(self) -> List[Product]:
        async with self.session_factory() as db:
            result = await db.execute(select(Product))
            return result.scalars().all()

    async def get_by_user(self, user_id: int) -> List[Product]:
        async with self.session_factory() as db:
            result = await db.execute(select(Product).filter(Product.user_id == user_id))
            return result.scalars().all()

    async def get_by_article_and_user(self, article: str, user_id: int) -> Optional[Product]:
        async with self.session_factory() as db:
            result = await db.execute(
                select(Product).filter(Product.article == article, Product.user_id == user_id)
            )
            return result.scalars().first()

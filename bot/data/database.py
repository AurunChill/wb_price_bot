from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_async_engine(settings.database.DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session


async def create_tables():
    from bot.data.models.user import User
    from bot.data.models.product import Product
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

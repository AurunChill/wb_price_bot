from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context

# Добавьте импорт ваших моделей
from bot.data.models.user import Base as UserBase
from bot.data.models.product import Base as ProductBase
from bot.data.models.allowed_users import Base as AllowedUserBase

config = context.config
fileConfig(config.config_file_name)

target_metadata = [UserBase.metadata, ProductBase.metadata, AllowedUserBase.metadata]


def run_migrations_online():
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True,  # Для SQLite
        )

        with context.begin_transaction():
            context.run_migrations()


async def run_async_migrations():
    await run_migrations_online()

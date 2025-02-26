from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from bot.data.models.allowed_users import AllowedUser


class AllowedUserService:
    def __init__(self, session: AsyncSession):
        self.session_factory = session

    async def add_user(self, user_id: int = None, username: str = None) -> AllowedUser:
        async with self.session_factory() as db:
            try:
                user = AllowedUser(user_id=user_id, username=username)
                db.add(user)
                await db.commit()
                return user
            except Exception:
                await db.rollback()
                raise

    async def remove_user_by_id(self, user_id: int) -> bool:
        async with self.session_factory() as db:
            try:
                result = await db.execute(
                    delete(AllowedUser).where(AllowedUser.user_id == user_id)
                )
                await db.commit()
                return result.rowcount > 0
            except Exception:
                await db.rollback()
                raise

    async def remove_user_by_username(self, username: str) -> bool:
        async with self.session_factory() as db:
            try:
                result = await db.execute(
                    delete(AllowedUser).where(AllowedUser.username == username)
                )
                await db.commit()
                return result.rowcount > 0
            except Exception:
                await db.rollback()
                raise

    async def is_allowed_by_id(self, user_id: int) -> bool:
        async with self.session_factory() as db:
            try:
                result = await db.execute(
                    select(AllowedUser).where(AllowedUser.user_id == user_id)
                )
                return result.scalar_one_or_none() is not None
            except Exception:
                await db.rollback()
                raise

    async def is_allowed_by_username(self, username: str) -> bool:
        async with self.session_factory() as db:
            try:
                result = await db.execute(
                    select(AllowedUser).where(AllowedUser.username == username)
                )
                return result.scalar_one_or_none() is not None
            except Exception:
                await db.rollback()
                raise

    async def get_all(self) -> List[AllowedUser]:
        async with self.session_factory() as db:
            result = await db.execute(select(AllowedUser))
            return result.scalars().all()

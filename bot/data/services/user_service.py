from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.data.models.user import User

class UserService:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def create(self, user: User) -> User:
        async with self.session_factory() as db:
            try:
                db.add(user)
                await db.commit()
                await db.refresh(user)
                return user
            except Exception:
                await db.rollback()
                raise

    async def delete(self, user_id: int) -> None:
        async with self.session_factory() as db:
            try:
                user = await db.get(User, user_id)
                if user:
                    await db.delete(user)
                    await db.commit()
            except Exception:
                await db.rollback()
                raise

    async def update(self, user_id: int, **kwargs) -> Optional[User]:
        async with self.session_factory() as db:
            try:
                user = await db.get(User, user_id)
                if user:
                    for key, value in kwargs.items():
                        if hasattr(user, key):
                            setattr(user, key, value)
                    await db.commit()
                    await db.refresh(user)
                return user
            except Exception:
                await db.rollback()
                raise

    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with self.session_factory() as db:
            return await db.get(User, user_id)
        
    async def get_by_username(self, username: str) -> Optional[User]:
        async with self.session_factory() as db:
            result = await db.execute(select(User).where(User.username == username.lower()))
            return result.scalar_one_or_none()

    async def get_all(self) -> List[User]:
        async with self.session_factory() as db:
            result = await db.execute(select(User))
            return result.scalars().all()
 
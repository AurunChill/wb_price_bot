from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from bot.data.models.allowed_users import AllowedUser


class AllowedUserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user_id: int = None, username: str = None) -> AllowedUser:
        user = AllowedUser(user_id=user_id, username=username)
        self.session.add(user)
        await self.session.commit()
        return user

    async def remove_user_by_id(self, user_id: int) -> bool:
        result = await self.session.execute(
            delete(AllowedUser).where(AllowedUser.user_id == user_id)
        )
        await self.session.commit()
        return result.rowcount > 0
    
    async def remove_user_by_username(self, username: str) -> bool:
        result = await self.session.execute(
            delete(AllowedUser).where(AllowedUser.username == username)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def is_allowed_by_id(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(AllowedUser).where(AllowedUser.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def is_allowed_by_username(self, username: str) -> bool:
        result = await self.session.execute(
            select(AllowedUser).where(AllowedUser.username == username)
        )
        return result.scalar_one_or_none() is not None

    async def get_all(self) -> List[AllowedUser]:
        result = await self.session.execute(select(AllowedUser))
        return result.scalars().all()

from sqlalchemy.orm import Session
from typing import List, Optional
from bot.data.models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        user = self.db.get(User, user_id)
        if user:
            self.db.delete(user)
            self.db.commit()

    def update(self, user_id: int, **kwargs) -> Optional[User]:
        user = self.db.get(User, user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

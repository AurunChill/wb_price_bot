from sqlalchemy import Column, Integer, String
from bot.data.database import Base


class AllowedUser(Base):
    __tablename__ = "allowed_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)
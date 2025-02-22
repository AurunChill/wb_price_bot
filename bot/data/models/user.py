from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from bot.data.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    link = Column(String)

    products = relationship("Product", back_populates="owner")

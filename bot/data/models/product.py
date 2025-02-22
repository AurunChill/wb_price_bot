from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from bot.data.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    article = Column(String, unique=True)
    name = Column(String)
    current_price = Column(Float)
    prev_price = Column(Float)          
    prev_price_date = Column(String)    
    stock = Column(Integer)
    image_url = Column(String)
    min_price = Column(Float)
    min_price_date = Column(String)
    max_price = Column(Float)
    max_price_date = Column(String)
    updated = Column(String)
    link = Column(String)
    
    owner = relationship("User", back_populates="products")
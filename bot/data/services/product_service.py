from sqlalchemy.orm import Session
from typing import List, Optional
from bot.data.models.product import Product


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> None:
        product = self.db.get(Product, product_id)
        if product:
            self.db.delete(product)
            self.db.commit()

    def update(self, product_id: int, **kwargs) -> Optional[Product]:
        product = self.db.get(Product, product_id)
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            self.db.commit()
            self.db.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.get(Product, product_id)

    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()

    def get_by_user(self, user_id: int) -> List[Product]:
        return self.db.query(Product).filter(Product.user_id == user_id).all()
    
    def get_by_article_and_user(self, article: str, user_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(
            Product.article == article,
            Product.user_id == user_id
        ).first()

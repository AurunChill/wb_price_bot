from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from config import settings


engine = create_engine(
    settings.database.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from bot.data.models.user import User
    from bot.data.models.product import Product
    Base.metadata.create_all(bind=engine)


db = next(get_db())
"""Модуль подключения к базе данных"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///example.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

async def get_db():
    """Подключение к базе данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

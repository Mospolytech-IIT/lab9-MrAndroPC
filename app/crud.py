"""Модуль CRUD запросов для БД"""
#pylint: disable=line-too-long
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import schemas, models

def create_user(db: Session, user: schemas.UserCreate):
    """Создание пользователя"""
    existing_user = db.query(models.User).filter((models.User.email == user.email) | (models.User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already exists")
    db_user = models.User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, post: schemas.PostBase, user_id: int):
    """Создание поста"""
    db_post = models.Post(title=post.title, content=post.content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_user(db: Session, user_id: int):
    """Получение пользователя"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получение пользователей"""
    return db.query(models.User).offset(skip).limit(limit).all()

def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Получение постов определенного пользователя"""
    return db.query(models.Post).filter(models.Post.user_id == user_id).offset(skip).limit(limit).all()

def get_posts_with_userinfo(db: Session, skip: int = 0, limit: int = 100):
    """Получение постов с информацией о пользователе"""
    return db.query(models.Post, models.User).join(models.User).offset(skip).limit(limit).all()

def update_user_email(db: Session, user_id: int, email: str):
    """Обновление email пользователя"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.email = email
    db.commit()
    db.refresh(db_user)
    return db_user

def update_post_content(db: Session, post_id: int, content: str):
    """Обновление контента поста"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db_post.content = content
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    """Удаление поста"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(db_post)
    db.commit()

def delete_user_with_posts(db: Session, user_id: int):
    """Удаление пользователя и его постов"""
    db_posts = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    for post in db_posts:
        db.delete(post)
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()

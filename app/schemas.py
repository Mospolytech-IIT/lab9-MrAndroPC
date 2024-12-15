"""Схемы для запросов"""
from pydantic import BaseModel

class PostBase(BaseModel):
    """Схема для поста"""
    title: str
    content: str

class Post(PostBase):
    """Схема для отображения поста"""
    id: int
    user_id: int

class UserBase(BaseModel):
    """Схема для пользователя"""
    username: str
    email: str

class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str

class User(UserBase):
    """Схема для отображения пользователя и постов"""
    id: int
    posts: list[Post] = []

class PostWithUserInfo(BaseModel):
    """Схема для отображения пользователя и поста"""
    post: Post
    user: User

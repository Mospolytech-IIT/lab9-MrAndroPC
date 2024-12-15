"""main.py"""
#pylint: disable=line-too-long
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app import models, schemas, crud, database

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    """Создаем базу данных и моковые данные при запуске"""    
    db = database.SessionLocal()
    # моковые данные
    if not db.query(models.User).first():
        user1 = crud.create_user(db, schemas.UserCreate(username="user1", email="user1@example.com", password="password1"))
        user2 = crud.create_user(db, schemas.UserCreate(username="user2", email="user2@example.com", password="password2"))
        crud.create_post(db, schemas.PostBase(title="Post 1", content="Content for post 1"), user_id=user1.id)
        crud.create_post(db, schemas.PostBase(title="Post 2", content="Content for post 2"), user_id=user2.id)

@app.get("/")
def read_root(request: Request, db: Session = Depends(database.get_db)):
    """Отображение главной страницы"""
    users = crud.get_users(db)
    posts = crud.get_posts_with_userinfo(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "users": users, "posts": posts}
    )

@app.get("/users/")
def list_users(request: Request, db: Session = Depends(database.get_db)):
    """Отображение списка пользователей"""    
    users = crud.get_users(db)
    return templates.TemplateResponse("list_users.html", {"request": request, "users": users})

@app.get("/users/new")
def new_user_form(request: Request):
    """Форма создания пользователя"""
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post("/users/new")
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db),
):
    """Создание пользователя"""
    crud.create_user(db, schemas.UserCreate(username=username, email=email, password=password))
    return RedirectResponse(url="/", status_code=303)

@app.get("/users/{user_id}/edit")
def edit_user_form(user_id: int, request: Request, db: Session = Depends(database.get_db)):
    """Форма редактирования пользователя"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.post("/users/{user_id}/edit")
def edit_user(
    user_id: int,
    email: str = Form(...),
    db: Session = Depends(database.get_db),
):
    """Редактирование пользователя"""
    crud.update_user_email(db, user_id, email)
    return RedirectResponse(url="/", status_code=303)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    """Удаление пользователя"""
    crud.delete_user_with_posts(db, user_id)
    return RedirectResponse(url="/", status_code=303)

@app.get("/posts/new")
def new_post_form(request: Request):
    """Форма создания поста"""
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/posts/new")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(database.get_db),
):
    """Создание поста"""
    crud.create_post(db, schemas.PostBase(title=title, content=content), user_id)
    return RedirectResponse(url="/", status_code=303)

@app.get("/posts/{post_id}/edit")
def edit_post_form(post_id: int, request: Request, db: Session = Depends(database.get_db)):
    """Форма редактирования поста"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})

@app.post("/posts/{post_id}/edit")
def edit_post(
    post_id: int,
    content: str = Form(...),
    db: Session = Depends(database.get_db),
):
    """Редактирование поста"""
    crud.update_post_content(db, post_id, content)
    return RedirectResponse(url="/", status_code=303)

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(database.get_db)):
    """Удаление поста"""
    crud.delete_post(db, post_id)
    return RedirectResponse(url="/", status_code=303)

@app.get("/posts/user/{user_id}", response_model=list[schemas.Post])
def get_user_posts(user_id: int, db: Session = Depends(database.get_db)):
    """Получение постов определенного пользователя"""
    return crud.get_posts_by_user(db, user_id)

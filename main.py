from datetime import date
from pathlib import Path

from fastapi import FastAPI,HTTPException, Request,status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
base_dir = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=base_dir / "templates")
app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static")


posts: list[dict] = [
    {
        "id": 1,
        "author": {
            "id": 1,
            "username": "Corey Schafer",
            "image_path": "/static/profile_pics/default.jpg",
        },
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": date(2025, 4, 20),
    },
    {
        "id": 2,
        "author": {
            "id": 2,
            "username": "Jane Doe",
            "image_path": "/static/profile_pics/default.jpg",
        },
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it ever",
        "date_posted": date(2025, 4, 21),
    }
]

@app.get("/",include_in_schema=False,name="home")
@app.get("/posts", include_in_schema=False,name="posts")
def home(request : Request):
    return templates.TemplateResponse(request,"home.html",{"posts": posts,"title": "Home"})


@app.get("/api/posts")
def get_posts():
    return {"posts": posts}

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/users/{user_id}", name="user_posts")
def user_posts(user_id: int):
    return {"user_id": user_id, "posts": [post for post in posts if post["author"]["id"] == user_id]}

@app.get("/posts/{post_id}", include_in_schema=False, name="post_page")
def post_page(request: Request, post_id: int):
    for post in posts:
        if post["id"] == post_id:
            title = post["title"]
            return templates.TemplateResponse(request,"post.html", {"post": post, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/account", name="account_page")
def account_page():
    return {"message": "Account page"}

@app.get("/login", name="login_page")
def login_page():
    return {"message": "Login page"}

@app.get("/register", name="register_page")
def register_page():
    return {"message": "Register page"}

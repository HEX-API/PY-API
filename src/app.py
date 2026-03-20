from fastapi import FastAPI, HTTPException
from src.schemas import PostCreate
from src.db import Post, create_db_and_tables, get_async_session

# to enable fastapi create the db upon startup
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan) # this will run the lifespan function upon app startup

text_post = {
    1: {"title": "Curious about FastAPI?", "content": "FastAPI is a modern, fast web framework for building APIs with Python 3.6+ based on standard Python type hints."},
    2: {"title": "Why choose FastAPI?", "content": "FastAPI is designed to be easy to use and learn, while also being powerful and efficient"},
    3: {"title": "Getting started with FastAPI", "content": "To get started with FastAPI"},
    4: {"title": "FastAPI features", "content": "FastAPI offers features such as automatic interactive API documentation, high performance, and easy integration with other libraries and tools."},

}

@app.get("/posts")
def get_all_posts(limit : int = None):
    if limit:
        return {key: text_post[key] for key in list(text_post.keys())[:limit]}

    return text_post

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in text_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_post.get(post_id)


@app.post("/posts")
def create_post(post : PostCreate) -> PostCreate:
    return post
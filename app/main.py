from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

import time

from . import models
from .database import engine
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi2",
            user="postgres",
            password="GarthNeele",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("DB connection was successful")
        break
    except Exception as error:
        print("DB Connection failure:")
        print("Error: ", error)
        time.sleep(2)


my_post = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "Proteins", "content": "all the proteins", "id": 2}
]


def find_post(id):
    for post in my_post:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, post in enumerate(my_post):
        if post["id"] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

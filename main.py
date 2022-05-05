from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "Proteins", "content": "all the proteins", "id": 2}
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_post}


@app.post("/posts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"data": "new post"}

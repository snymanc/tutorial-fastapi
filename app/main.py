from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, post, user

# Creates tables specified in models.py
# if tables don't exists
# will not update existing table
# if table is updated in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}

from fastapi import FastAPI
from .database import engine
from .import models
from .routers import blog,user


app = FastAPI(title="Routers in FastAPI")

#Creating all database table
models.Base.metadata.create_all(bind=engine)


app.include_router(blog.router)
app.include_router(user.router)

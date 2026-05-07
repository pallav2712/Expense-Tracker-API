from fastapi import FastAPI

from .routers import expenses
from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(expenses.router)

@app.get("/")
def root():
    return {"message": "Hello World, this is my root for expense api"}
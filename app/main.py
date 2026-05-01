from fastapi import FastAPI

from app.routers import expenses

app = FastAPI()

app.include_router(expenses.router)

@app.get("/")
def root():
    return {"message": "Hello World, this is my root for expense api"}
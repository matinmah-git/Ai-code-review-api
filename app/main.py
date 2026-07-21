from fastapi import FastAPI

from app.database.database import Base, engine

from app.api.auth import router as auth_router
from app.api.reviews import router as review_router

from app.models.user import User
from app.models.review import Review
from app.models.job import Job

Base.metadata.create_all(bind=engine)
app = FastAPI(title= "AI Code Review API",)

app.include_router(auth_router, prefix="/api")
app.include_router(review_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to the AI Code Review API!"}

import json
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

from app.models.review import Review
from app.schemas.analysis import SnippetReviewRequest, GithubReviewRequest
from app.database.database import get_db
from app.schemas.analysis import ReviewResponse
from app.services.file_service import FileService
from app.services.ai_service import AIService
from app.services.github_service import GithubService
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/reviews", tags=["reviews"])


def get_ai_service():
    return AIService()

def get_file_service():
    return FileService()

def get_github_service():
    return GithubService()


@router.get("/", response_model=list[ReviewResponse])
def get_reviews(current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):

    reviews = db.query(Review).filter(Review.user_id == current_user.id).order_by(Review.created_at.desc()).all()

    if reviews is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No review found")

    return reviews


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int,
               current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db),
               ):

    review = db.query(Review).filter(and_(Review.user_id == current_user.id, Review.id == review_id)).first()

    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    return review


@router.post("/snippet", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_snippet(request: SnippetReviewRequest,
                   current_user: User = Depends(get_current_user),
                   ai_service: AIService = Depends(get_ai_service),
                   db: Session = Depends(get_db)
                   ):

    ai_review = ai_service.review_code(project_name=request.project_name , code=request.code)

    review = Review(user_id=current_user.id, title=request.project_name, code=request.code, ai_review=json.dumps(ai_review))

    db.add(review)
    db.commit()
    db.refresh(review)

    return review

@router.post("/github", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_github(request: GithubReviewRequest,
                  current_user: User = Depends(get_current_user),
                  ai_service: AIService = Depends(get_ai_service),
                  github_service: GithubService = Depends(get_github_service),
                  db: Session = Depends(get_db)):

    repo_name = github_service.get_repository_name(request.repository_url)
    repo_code = github_service.read_repository(request.repository_url)
    ai_review = ai_service.review_code(project_name=repo_name, code=repo_code)

    review = Review(user_id=current_user.id, title=repo_name, repository_url=request.repository_url ,code=repo_code, ai_review=json.dumps(ai_review) )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review

@router.post("/upload", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_upload(file: UploadFile = File(...),
                  current_user: User = Depends(get_current_user),
                  file_service: FileService = Depends(get_file_service),
                  ai_service: AIService = Depends(get_ai_service),
                  db: Session = Depends(get_db)
                  ):

    code = file_service.read_uploaded_file(file)

    ai_review = ai_service.review_code(project_name=file.filename, code=code)

    review = Review(user_id=current_user.id, code=code, title=file.filename , ai_review=json.dumps(ai_review) )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


@router.post("/archive", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_archive(file: UploadFile = File(...),
                   current_user: User = Depends(get_current_user),
                   file_service: FileService = Depends(get_file_service),
                   ai_service: AIService = Depends(get_ai_service),
                   db: Session = Depends(get_db)
                   ):
    code = file_service.read_archive(file)

    ai_review = ai_service.review_code(project_name=file.filename, code=code)

    review = Review(user_id=current_user.id, title=file.filename, code=code , ai_review=json.dumps(ai_review) )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review

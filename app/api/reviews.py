from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schemas.analysis import ReviewResponse
from app.services.review_service import ReviewService
from app.services.file_service import FileService
from app.services.ai_service import AIService
from app.services.github_service import GithubService
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(prefix="/reviews", tags=["reviews"])


def get_review_service(db: Session = Depends(get_db) ):
    return ReviewService(db=db, ai_service=AIService(), github_service=GithubService(), file_service=FileService())



@router.get("/", response_model=list[ReviewResponse])
def get_reviews(current_user: User = Depends(get_current_user),service: ReviewService = Depends(get_review_service)):

    return service.get_reviews(current_user=current_user)


@router.get("/review_id", response_model=ReviewResponse)
def get_review(review_id: int, current_user: User = Depends(get_current_user), service: ReviewService = Depends(get_review_service)):

    return service.get_review( current_user=current_user, review_id=review_id)


@router.post("/snippet", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_snippet(request: SnippetReviewRequest, current_user: User = Depends(get_current_user), service: ReviewService = Depends(get_review_service)):

    return service.review_snippet(current_user=current_user, request=request)


@router.post("/github", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_github(request: GithubReviewRequest, current_user: User = Depends(get_current_user), service: ReviewService = Depends(get_review_service)):

    return service.review_github(current_user=current_user, request=request)


@router.post("/upload", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_upload(file: UploadFile = File(...), current_user: User = Depends(get_current_user), service: ReviewService = Depends(get_review_service)):

    return service.review_uploaded_file(current_user=current_user, file=file)


@router.post("/archive", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_archive(file: UploadFile = File(...), current_user: User = Depends(get_current_user), service: ReviewService = Depends(get_review_service)):
    return service.review_archive(current_user=current_user, file=file)

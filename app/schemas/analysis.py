from pydantic import BaseModel, HttpUrl
from datetime import datetime


class SnippetReviewRequest(BaseModel):
    code: str


class GithubReviewRequest(BaseModel):
    repository_url: HttpUrl


class JobResponse(BaseModel):
    id: int
    name: str
    status: str
    provider: str
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    message: str
    job_id: int


class ReviewResponse(BaseModel):
    id: int
    job_id: int | None
    repository_url: str | None
    code: str | None
    ai_review: dict
    created_at: datetime

    class Config:
        from_attributes = True
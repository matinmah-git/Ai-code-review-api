from pydantic import BaseModel, validator
from datetime import datetime
import json

class SnippetReviewRequest(BaseModel):
    project_name: str
    code: str


class GithubReviewRequest(BaseModel):
    repository_url: str



class ReviewResponse(BaseModel):
    id: int
    title: str
    repository_url: str | None
    code: str | None
    ai_review: dict
    created_at: datetime

    @validator("ai_review", pre=True)
    def parse_ai_review(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return v

    class Config:
        from_attributes = True
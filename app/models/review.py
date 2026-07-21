from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime,timezone
from sqlalchemy.orm import relationship

from app.database.database import Base


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id =  Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete="SET NULL"), nullable=True, index=True)
    repository_url = Column(String(500), nullable=True)
    code = Column(Text, nullable=False)
    ai_review = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="reviews")
    job = relationship("Job", back_populates="review")
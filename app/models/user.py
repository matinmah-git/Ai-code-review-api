from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Relationship
from datetime import datetime, timezone

from app.database.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    hashed_password = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False, default='member')
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    reviews = Relationship("Review", back_populates="user", cascade="all, delete-orphan")
    jobs = Relationship("Job", back_populates="user")
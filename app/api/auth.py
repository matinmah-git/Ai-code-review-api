from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserCreate, UserLogin, TokenResponse
from app.database.database import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_services(db: Session = Depends(get_db)):
    return AuthService(db)


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, service: AuthService = Depends(get_auth_services)):
    return service.register_user(user_data)

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, service: AuthService = Depends(get_auth_services)):
    return service.login_user(user_data)


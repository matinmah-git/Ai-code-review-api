from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse


class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: UserCreate) -> User:

        if self.db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        if self.db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        new_user = User(username=user_data.username, email=user_data.email, hashed_password=hash_password(user_data.password))

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except Exception:
            self.db.rollback()
            raise

        return new_user

    def login_user(self, user_data: UserLogin) :

        user = self.db.query(User).filter(User.username == user_data.username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")

        if not verify_password(user_data.password, str(user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")

        #if not user.is_verified:
        #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please verify your email")

        data = {"sub": str(user.id), "role": user.role}
        token = create_access_token(data)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
        )

    #def verify_email(...):


    #def resend_verification_code(...):


    #def change_password(...):

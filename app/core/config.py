from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    AI_API_KEY: str
    AI_BASE_URL: str
    AI_MODEL: str

    UPLOAD_DIRECTORY: str = "uploads"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
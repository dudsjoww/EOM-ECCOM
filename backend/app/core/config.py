from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()

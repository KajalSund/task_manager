# app/config.py
from pydantic_settings import BaseSettings  # Updated import
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env into os.environ

DATABASE_URL = os.getenv("DATABASE_URL")

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

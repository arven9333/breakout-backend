#!/usr/bin/python3

import hashlib
import os
from typing import Optional

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path


class PgDriverConfig(BaseSettings):
    prepare_threshold: Optional[int] = None  # If it is set to None, prepared statements are disabled on the connection.


class PgDbConfig(BaseSettings):
    DB_ECHO_LOG: bool = False

    pg_driver_config: PgDriverConfig = PgDriverConfig()

    PG_MASTER_DRIVER: str = os.getenv("PG_MASTER_DRIVER", "postgresql+asyncpg")
    PG_MASTER_USER: str = os.getenv("PG_MASTER_USER", "postgres")
    PG_MASTER_PASSWORD: str = os.getenv("PG_MASTER_PASSWORD", "postgres")
    PG_MASTER_HOST: str = os.getenv("PG_MASTER_HOST", "postgres")
    PG_MASTER_PORT: int = int(os.getenv("PG_MASTER_PORT", "5432"))
    PG_MASTER_DB: str = os.getenv("PG_MASTER_DB", "postgres")

    @property
    def db_master_uri(self) -> str:
        return (
            f"postgresql+{self.PG_MASTER_DRIVER}://{self.PG_MASTER_USER}:"
            f"{self.PG_MASTER_PASSWORD}@{self.PG_MASTER_HOST}:{self.PG_MASTER_PORT}/"
            f"{self.PG_MASTER_DB}"
        )

    @property
    def db_master_uri_migrations(self) -> str:
        driver = self.PG_MASTER_DRIVER
        if driver == 'postgresql+asyncpg':
            driver = 'psycopg2'

        return (
            f"postgresql+{driver}://{self.PG_MASTER_USER}:"
            f"{self.PG_MASTER_PASSWORD}@{self.PG_MASTER_HOST}:{self.PG_MASTER_PORT}/"
            f"{self.PG_MASTER_DB}"
        )


class ApiConfig(BaseSettings):
    SHOW_DOCS: bool = True
    API_ROOT: str = ''
    BACK_HOST: str = '0.0.0.0'
    BACK_PORT: int = 8000
    UVICORN_WORKERS_COUNT: int = 1
    UVICORN_LOG_LEVEL: str = 'debug'
    UVICORN_RELOAD: bool = True


class Settings(BaseSettings):
    DEBUG: bool = False
    ENABLE_LOG_REQUESTS: bool = False
    JWT_SECRET_KEY: str = hashlib.sha256(b"secret key").hexdigest()

    api_config: ApiConfig = ApiConfig()
    pg_db_config: PgDbConfig = PgDbConfig()


BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOCAL_HOST = os.getenv("LOCAL_HOST", "http://localhost:8000")

FRONT_HOST = os.getenv("FRONT_HOST", "http://localhost:3000")
FRONT_LOGIN_PAGE = FRONT_HOST + "/auth/login"
FRONT_FORGET_PASSWORD_URL = FRONT_HOST + "/auth/login"

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "1"))


SRC_DIR = BASE_DIR / 'src'
IMAGES_DIR = SRC_DIR / 'images'
ICONS_DIR = IMAGES_DIR / 'icons'
MAPS_DIR = IMAGES_DIR / 'maps'

TWITCH_LINK_OAUTH = "https://id.twitch.tv/oauth2/authorize"
GOOGLE_LINK_OAUTH = "https://accounts.google.com/o/oauth2/auth"

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID", "some_twitch_key")
TWITCH_SECRET = os.getenv("TWITCH_SECRET", "some_twitch_key")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "some_google_key")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "some_google_key")

ENDPOINT_CALLBACK = "api/v1/user/auth/callback"
GOOGLE_REDIRECT_URL = f"{LOCAL_HOST}/{ENDPOINT_CALLBACK}/google/handle"
TWITCH_REDIRECT_URL = f"{LOCAL_HOST}/{ENDPOINT_CALLBACK}/twitch"

TWITCH_REDIRECT_LINK = f"{TWITCH_LINK_OAUTH}?response_type=token&client_id={TWITCH_CLIENT_ID}&redirect_uri={TWITCH_REDIRECT_URL}"
GOOGLE_REDIRECT_LINK = f"{GOOGLE_LINK_OAUTH}?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URL}&response_type=code&scope=openid email profile"

EMAIL = os.getenv("EMAIL", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_password")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "465"))

STREAMER_NAME = os.getenv("STREAMER_NAME", "arven93")

if load_dotenv(str(BASE_DIR / '.env')) is False:
    raise AssertionError(f"File .env not found, search directory: {BASE_DIR / '.env'}")

settings = Settings()

import hashlib
import os
from typing import Optional

import orjson

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


class RedisConfig(BaseSettings):
    REDIS_NAMESPACE: str = os.getenv("REDIS_NAMESPACE", "redis")
    REDIS_NODES: str = '[]'

    @property
    def redis_cluster_nodes(self) -> list:
        return orjson.loads(self.REDIS_NODES)


class Settings(BaseSettings):
    DEBUG: bool = False
    ENABLE_LOG_REQUESTS: bool = False
    JWT_SECRET_KEY: str = hashlib.sha256(b"secret key").hexdigest()

    api_config: ApiConfig = ApiConfig()
    pg_db_config: PgDbConfig = PgDbConfig()


BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / 'src'
IMAGES_DIR = SRC_DIR / 'images'
ICONS_DIR = IMAGES_DIR / 'icons'
MAPS_DIR = IMAGES_DIR / 'maps'

if load_dotenv(str(BASE_DIR / '.env')) is False:
    raise AssertionError(f"File .env not found, search directory: {BASE_DIR / '.env'}")

settings = Settings()

from __future__ import annotations

import functools

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.apps.common.logic.common import get_env_path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_path(), env_file_encoding="utf-8", env_prefix="", extra="ignore")
    SERVER_TZ: str = "UTC"
    IS_DEBUG: bool = False
    IS_TESTING_MODE: bool = False
    CORS_ORIGINS: str = ""

    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 63791
    REDIS_DB: int = 1

    DB_USER: str = "admin"
    DB_PASSWORD: str = "admin"
    DB_NAME: str = "feature_switch_db"
    DB_HOST: str = ""
    DB_PORT: int = 5432
    TEST_DB_USER: str = ""
    TEST_DB_PASSWORD: str = ""


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()


@functools.lru_cache
def get_cors_origins():
    settings = get_settings()
    cors_origins_str = settings.CORS_ORIGINS
    return [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

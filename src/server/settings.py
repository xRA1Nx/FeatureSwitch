from __future__ import annotations

import functools

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.apps.common.logic.common import get_env_path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_path(), env_file_encoding="utf-8", env_prefix="", extra="ignore")
    SERVER_TZ: str = "UTC"
    IS_DEBUG: bool = False
    IS_TESTING_MODE: bool = False


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()

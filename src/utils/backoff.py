from __future__ import annotations

from src.server.settings import get_settings


def backoff_max_tries(value: int) -> int:
    settings = get_settings()
    if settings.IS_TESTING_MODE is True:
        return 1
    return value

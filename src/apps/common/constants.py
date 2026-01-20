from __future__ import annotations

from pathlib import Path
from zoneinfo import ZoneInfo


BASE_DIR = Path(__file__).parent.parent.parent.parent

POSTGRES_DB_URL_PREFIX = "postgresql"
POSTGRES_DB_URL_ASYNC_PREFIX = "postgresql+asyncpg"

MOSCOW_TZ = ZoneInfo("Europe/Moscow")
UTC_TZ = ZoneInfo("UTC")

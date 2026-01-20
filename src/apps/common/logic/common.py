from __future__ import annotations

import os.path

from src.apps.common.constants import BASE_DIR


def get_env_path() -> str:
    expected_path = os.path.join("/app", ".env")
    if os.path.exists(expected_path):
        return expected_path
    return os.path.join(BASE_DIR, ".env")

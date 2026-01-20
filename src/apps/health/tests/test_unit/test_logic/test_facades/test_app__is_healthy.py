from __future__ import annotations

import pytest
from app.health.logic.facades import app__is_healthy


@pytest.mark.asyncio
async def test__app__is_healthy():
    test_result = await app__is_healthy()

    assert test_result is True

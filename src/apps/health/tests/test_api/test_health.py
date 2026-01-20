from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test__health__200(api_client, mocked__app__is_healthy):
    mocked__app__is_healthy.return_value = True
    expected_content = b'{"status":"ok"}'

    response = api_client.get("/api/health")

    assert response.status_code == 200
    assert response.content == expected_content
    mocked__app__is_healthy.assert_called_once_with()


@pytest.mark.asyncio
async def test__health__500(api_client, mocked__app__is_healthy):
    mocked__app__is_healthy.return_value = False
    expected_content = b'"undefined_error"'

    response = api_client.get("/api/health")

    assert response.status_code == 500
    assert response.content == expected_content
    mocked__app__is_healthy.assert_called_once_with()

from __future__ import annotations

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.server.settings import get_settings


class SimpleAuth(AuthenticationBackend):
    """Самая простая проверка логина/пароля"""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        settings = get_settings()

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session["authenticated"] = True
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.pop("authenticated", None)
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("authenticated", False)

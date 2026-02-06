from __future__ import annotations

from fastapi import FastAPI
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.apps.admin.team import TeamAdmin, TeamServiceAdmin
from src.apps.admin.feature_flag import FeatureFlagAdmin
from src.server.db import get_async_engine
from src.server.settings import get_settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        settings = get_settings()

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"admin": True})
            return True
        return False

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin", False)

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True


def initialise_admin_panel(*, app: FastAPI) -> Admin:
    admin = Admin(
        app=app,
        engine=get_async_engine(),
        authentication_backend=AdminAuth(secret_key="change-in-production"),
        base_url="/admin",
        title="Feature Flags Admin",
    )
    admin.add_view(FeatureFlagAdmin)
    admin.add_view(TeamAdmin)
    admin.add_view(TeamServiceAdmin)
    return admin

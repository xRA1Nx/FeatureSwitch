from __future__ import annotations

import typing

from fastapi import FastAPI
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.apps.admin.feature_flag import FeatureFlagAdmin
from src.apps.admin.team import TeamAdmin, TeamServiceAdmin
from src.apps.admin.user import UserAdmin
from src.apps.user.logic.selectors.user import user__find_by_email
from src.server.db import get_async_engine
from src.utils.password import verify_password


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = typing.cast(str, form.get("username"))
        password = typing.cast(str, form.get("password"))

        if not email or not password:
            return False

        user = await user__find_by_email(email=email)

        if not user or not user.is_active:
            return False

        if not verify_password(raw_password=password, hashed=user.hashed_password):
            return False

        request.session.update({"authenticated": True, "user_id": user.id, "email": user.email})
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("authenticated", False)

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
    admin.add_view(UserAdmin)
    return admin

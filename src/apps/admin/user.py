from __future__ import annotations

from sqladmin import ModelView
from starlette.requests import Request

from src.apps.common.custom_types import GenericContext
from src.apps.user.models import User
from src.utils.password import get_hashed_password
from src.utils.strings import ensure_valid_email


class UserAdmin(ModelView, model=User):
    column_details_list = "__all__"
    column_default_sort = [("id", True)]
    column_searchable_list = ["email"]
    column_sortable_list = ["id", "email", "is_admin", "is_active", "created_at"]
    column_list = ["id", "email", "is_admin", "is_active"]

    form_create_rules = ["email", "password", "is_active"]
    form_edit_rules = ["email", "is_active"]

    form_excluded_columns = ["hashed_password"]

    async def on_model_change(self, data: GenericContext, model: User, is_created: bool, request: Request) -> None:
        if is_created and "password" in data:
            raw_password = data.pop("password")
            data["hashed_password"] = get_hashed_password(raw_password)
            data["is_admin"] = False

        if "email" in data:
            email = data["email"].strip().lower()
            ensure_valid_email(email=email, should_raise_exception=True)
            data["email"] = email

        return await super().on_model_change(data=data, model=model, is_created=is_created, request=request)

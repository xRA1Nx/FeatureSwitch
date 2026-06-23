from __future__ import annotations

from sqladmin import ModelView
from starlette.requests import Request
from wtforms.validators import DataRequired

from src.apps.common.custom_types import GenericContext
from src.apps.user.models import User
from src.utils.password import get_hashed_password
from src.utils.strings import ensure_valid_email


class UserAdmin(ModelView, model=User):
    column_details_exclude_list = ["hashed_password"]

    column_default_sort = [("id", True)]
    column_searchable_list = ["email"]
    column_sortable_list = ["id", "email", "is_admin", "is_active", "created_at"]
    column_list = ["id", "email", "is_admin", "is_active"]

    column_labels = {"hashed_password": "Password"}

    form_create_rules = ["email", "hashed_password", "team"]
    form_edit_rules = ["email", "team", "is_active"]

    form_args = {"team": {"validators": [DataRequired()]}}

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("is_admin", False) and request.session.get("is_active", False)

    async def on_model_change(self, data: GenericContext, model: User, is_created: bool, request: Request) -> None:
        if is_created:
            raw_password = data.pop("hashed_password", None)
            if not raw_password:
                raise ValueError("Password is required for new users")

            data["hashed_password"] = get_hashed_password(raw_password=raw_password)
            data["is_admin"] = False
            data["is_active"] = True

        if "email" in data:
            email = data["email"].strip().lower()
            ensure_valid_email(email=email, should_raise_exception=True)
            data["email"] = email

        return await super().on_model_change(data=data, model=model, is_created=is_created, request=request)

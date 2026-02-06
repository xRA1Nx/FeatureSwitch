from __future__ import annotations

from sqladmin import ModelView
from starlette.requests import Request

from src.apps.common.custom_types import GenericContext
from src.apps.team.models import Team, TeamService


class TeamAdmin(ModelView, model=Team):
    column_details_list = "__all__"
    column_list = ["name"]
    form_columns = ["name"]

    async def on_model_change(self, data: dict, model: Team, is_created: bool, request: Request) -> None:
        data = self._get_clean_data(data=data)
        return await super().on_model_change(data=data, model=model, is_created=is_created, request=request)

    @staticmethod
    def _get_clean_data(data: GenericContext) -> GenericContext:
        name: str | None = data.get("name")
        if name:
            data["name"] = name.upper().strip()
        return data


class TeamServiceAdmin(ModelView, model=TeamService):
    column_details_list = "__all__"
    column_list = ["name", "team"]
    form_columns = ["name", "team"]

    async def on_model_change(self, data: dict, model: TeamService, is_created: bool, request: Request) -> None:
        data = self._get_clean_data(data=data)
        return await super().on_model_change(data=data, model=model, is_created=is_created, request=request)

    @staticmethod
    def _get_clean_data(data: dict) -> GenericContext:
        name: str | None = data.get("name")
        if name:
            data["name"] = name.upper().strip()
        return data

from __future__ import annotations

from sqladmin import ModelView

from src.apps.team.models import Team, TeamService


class TeamAdmin(ModelView, model=Team):
    column_details_list = "__all__"
    column_list = ["name"]
    form_columns = ["name"]


class TeamServiceAdmin(ModelView, model=TeamService):
    column_details_list = "__all__"
    column_list = ["name", "team"]
    form_columns = ["name", "team"]

from __future__ import annotations

from fastapi import Request
from sqladmin import ModelView

from src.apps.feature_flag.dtos import FeatureFlagUpdateDto
from src.apps.feature_flag.logic.facades.feature_flag import feature_flag__update
from src.apps.feature_flag.models import FeatureFlag


class FeatureFlagAdmin(ModelView, model=FeatureFlag):
    column_details_list = "__all__"
    column_list = ["name", "team_service", "is_active", "activated_at"]
    form_create_rules = ["name", "team_service", "ttl_days"]
    form_edit_rules = ["is_active", "ttl_days"]

    async def on_model_change(
        self, data: dict, model: FeatureFlag, is_created: bool, request: Request
    ) -> None:
        update_dto = FeatureFlagUpdateDto.model_validate(data)
        await feature_flag__update(updated_feature_flag=model, update_dto=update_dto)

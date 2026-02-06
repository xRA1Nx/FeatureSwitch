from __future__ import annotations

from fastapi import Request
from sqladmin import ModelView

from src.apps.common.custom_types import GenericContext
from src.apps.feature_flag.dtos import FeatureFlagUpdateDto
from src.apps.feature_flag.logic.facades.feature_flag import feature_flag__prepare_for_admin_update
from src.apps.feature_flag.models import FeatureFlag


class FeatureFlagAdmin(ModelView, model=FeatureFlag):
    column_details_list = "__all__"
    column_list = ["name", "team_service", "is_active", "activated_at"]
    form_create_rules = ["name", "team_service", "ttl_days"]
    form_edit_rules = ["is_active", "ttl_days"]

    async def on_model_change(self, data: dict, model: FeatureFlag, is_created: bool, request: Request) -> None:
        data = self._get_clean_data(data=data)
        if is_created:
            return await self._on_create_action(data=data, model=model, is_created=is_created, request=request)
        return await self._on_update_action(data=data, model=model, is_created=is_created, request=request)

    @staticmethod
    def _get_clean_data(data: dict) -> GenericContext:
        name: str | None = data.get("name")
        if name:
            data["name"] = name.upper().strip()
        return data

    async def _on_create_action(self, data: dict, model: FeatureFlag, is_created: bool, request: Request) -> None:
        return await super().on_model_change(data=data, model=model, is_created=is_created, request=request)


    async def _on_update_action(self, data: dict, model: FeatureFlag, is_created: bool, request: Request) -> None:
        update_dto = FeatureFlagUpdateDto.model_validate(data)
        model = await feature_flag__prepare_for_admin_update(updated_feature_flag=model, update_dto=update_dto)
        if not model:
            return None
        return await super().on_model_change(data=data, model=model, is_created=is_created, request=request)

from __future__ import annotations

from sqladmin import ModelView

from src.apps.feature_flags.models import FeatureFlag


class FeatureFlagAdmin(ModelView, model=FeatureFlag):
    column_details_list = "__all__"
    column_list = ["name", "team_service", "is_active", "activated_at"]
    form_create_rules = ["name", "team_service", "ttl_days"]
    form_edit_rules = ["is_active", "ttl_days"]

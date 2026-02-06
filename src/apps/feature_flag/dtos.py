from __future__ import annotations

import datetime

from src.apps.common.dto import BaseDto


class FeatureFlagUpdateDto(BaseDto):
    is_active: bool | None = None
    ttl_days: int | None = None


class FeatureFlagListRequestDto(BaseDto):
    is_active: bool | None = None
    team_name: str | None = None
    service_name: str | None = None


class FeatureFlagListItemDto(BaseDto):
    name: str
    is_active: bool
    ttl_days: int
    activated_at: datetime.datetime | None


class FeatureFlagFilterDto(BaseDto):
    is_active: bool | None = None
    service_id: int | None = None
    team_service_ids: list[int] | None = None

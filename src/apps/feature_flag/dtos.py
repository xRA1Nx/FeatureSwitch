from __future__ import annotations

import datetime

from src.apps.common.dtos import BaseDto


class FeatureFlagUpdateDto(BaseDto):
    is_active: bool | None = None
    ttl_days: int | None = None


class FeatureFlagListRequestDto(BaseDto):
    is_active: bool | None = None
    is_expired: bool | None = None

    name: str | None = None
    team_name: str | None = None
    service_name: str | None = None


class FeatureFlagFilterDto(BaseDto):
    is_expired: bool | None = None
    is_active: bool | None = None

    service_id: int | None = None
    team_id: int | None = None
    name: str | None = None


class FeatureFlagDto(BaseDto):
    id: int
    name: str
    is_active: bool
    ttl_days: int
    activated_at: datetime.datetime | None
    team_service_id: int

from src.apps.common.dto import BaseDto


class FeatureFlagUpdateDto(BaseDto):
    is_active: bool | None = None
    ttl_days: int | None = None
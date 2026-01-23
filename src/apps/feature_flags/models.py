from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.common.models import BaseModel
from src.apps.groups.models import Group
from src.server.settings import get_settings


settings = get_settings()


class FeatureFlag(BaseModel):
    name: Mapped[int] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=False, server_default="false")
    ttl_days: Mapped[int] = mapped_column(default=settings.FLAG_TTL_DAYS, server_default=str(settings.FLAG_TTL_DAYS))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped[Group] = relationship("Group", back_populates="feature_flags")

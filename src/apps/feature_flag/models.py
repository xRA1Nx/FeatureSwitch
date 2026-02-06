from __future__ import annotations

import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.common.models import BaseModel
from src.apps.team.models import TeamService
from src.server.settings import get_settings


settings = get_settings()


class FeatureFlag(BaseModel):
    name: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=False, server_default="false")
    ttl_days: Mapped[int] = mapped_column(default=settings.FLAG_TTL_DAYS, server_default=str(settings.FLAG_TTL_DAYS))

    activated_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    team_service_id: Mapped[int] = mapped_column(ForeignKey("teamservices.id"))
    team_service: Mapped[TeamService] = relationship("TeamService", back_populates="feature_flags")

    def __str__(self) -> str:
        return self.name

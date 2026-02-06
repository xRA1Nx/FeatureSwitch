from __future__ import annotations

import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.common.models import BaseModel


if typing.TYPE_CHECKING:
    from src.apps.feature_flag.models import FeatureFlag


class Team(BaseModel):
    name: Mapped[str] = mapped_column(unique=True)

    team_services: Mapped[list[TeamService]] = relationship(back_populates="team")

    def __str__(self) -> str:
        return self.name


class TeamService(BaseModel):
    name: Mapped[str] = mapped_column(unique=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team: Mapped[Team] = relationship("Team", back_populates="team_services")

    feature_flags: Mapped[list[FeatureFlag]] = relationship(back_populates="team_service")

    def __str__(self) -> str:
        return self.name

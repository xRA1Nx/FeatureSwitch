from __future__ import annotations

import typing

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.common.models import BaseModel


if typing.TYPE_CHECKING:
    from src.apps.team.models import Team


class User(BaseModel):
    __table_args__ = (CheckConstraint("(is_admin = true) OR (team_id IS NOT NULL)", name="non_admin_must_have_team"),)

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    is_admin: Mapped[bool] = mapped_column(default=False, server_default="false")
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id", ondelete="RESTRICT"), nullable=True)
    team: Mapped[Team | None] = relationship("Team", back_populates="users")

    def __str__(self) -> str:
        return self.email

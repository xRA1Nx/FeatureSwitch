from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from src.apps.common.models import BaseModel


class User(BaseModel):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

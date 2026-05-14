from __future__ import annotations

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(*, raw_password: str) -> str:
    return pwd_context.hash(raw_password)


def verify_password(*, raw_password: str, hashed: str) -> bool:
    return pwd_context.verify(raw_password, hashed)

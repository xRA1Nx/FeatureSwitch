from __future__ import annotations

import typing

from src.apps.common.dto import BaseDto
from src.apps.common.models import BaseModel


GenericContext = dict[str, typing.Any]
ListGenericContext = list[GenericContext]

BaseDtoType = typing.TypeVar("BaseDtoType", bound=BaseDto)
BaseModelType = typing.TypeVar("BaseModelType", bound=BaseModel)


class _EmptySentinel:
    """Пустота"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "<EMPTY>"


EMPTY: typing.Final = _EmptySentinel()

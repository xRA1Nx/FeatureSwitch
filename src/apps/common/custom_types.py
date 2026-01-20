from __future__ import annotations

import typing

from src.common.dto import BaseDto
from src.common.models import BaseModel


GenericContext = dict[str, typing.Any]
ListGenericContext = list[GenericContext]


BaseDtoType = typing.TypeVar("BaseDtoType", bound=BaseDto)
BaseModelType = typing.TypeVar("BaseModelType", bound=BaseModel)

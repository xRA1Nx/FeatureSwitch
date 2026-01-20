from __future__ import annotations

import datetime
import typing

from pydantic import BaseModel, ConfigDict


class BaseDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True, from_attributes=True, frozen=True)


class BaseDtoWithAliases(BaseDto):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, use_enum_values=True, from_attributes=True, frozen=True, populate_by_name=True
    )


class CommonSuccessResponseDto(BaseDto):
    status: typing.Literal["ok"] = "ok"


class FailContentForTestsDto(BaseDto):
    content: str
    path: str


class VideoTrimIntervalDto(BaseDto):
    start_since_seconds: float
    end_at_seconds: float


class IntervalDto(BaseDto):
    start_at: datetime.datetime
    end_at: datetime.datetime


class TimeIntervalDto(BaseDto):
    start_at: datetime.time
    end_at: datetime.time


class KafkaDto(BaseDto):
    key: str
    bucket_name: str
    source_path: str

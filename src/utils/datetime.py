from __future__ import annotations

import datetime
import functools
import time
import typing
from functools import wraps
from logging import getLogger
from zoneinfo import ZoneInfo

from src.apps.common.constants import HALF_OF_HOUR_IN_MINUTES, HOUR_IN_MINUTES, QUARTER_OF_HOUR_IN_MINUTES
from src.apps.common.dto import TimeIntervalDto
from src.server.settings import get_settings


logger = getLogger(__name__)


@functools.lru_cache
def get_server_timezone() -> ZoneInfo:
    settings = get_settings()
    return ZoneInfo(settings.SERVER_TZ)


@functools.lru_cache
def get_moscow_timezone() -> ZoneInfo:
    return ZoneInfo("Europe/Moscow")


def datetime_now_with_server_tz() -> datetime.datetime:
    return datetime.datetime.now(tz=get_server_timezone())


def datetime_now_with_moscow_tz() -> datetime.datetime:
    return datetime.datetime.now(tz=get_moscow_timezone())


def get_datetime_field_value_with_tz(*, datetime_field: datetime.datetime) -> datetime.datetime:
    server_tz = get_server_timezone()
    if datetime_field.tzinfo is None:
        return datetime_field.replace(tzinfo=server_tz)
    return datetime_field.astimezone(tz=server_tz)


def get_tomorrow_date_with_server_tz() -> datetime.date:
    return datetime_now_with_server_tz().date() + datetime.timedelta(days=1)


def get_start_of_date_with_server_tz(start_at: datetime.date) -> datetime.datetime:
    """Formate datetime object with start of date time from date object."""
    return datetime.datetime.combine(start_at, datetime.time.min, tzinfo=get_server_timezone())


def get_start_of_date_with_moscow_tz(start_at: datetime.date) -> datetime.datetime:
    """Formate datetime object with start of date time from date object."""
    return datetime.datetime.combine(start_at, datetime.time.min, tzinfo=get_moscow_timezone())


def get_end_of_date_with_server_tz(start_at: datetime.date) -> datetime.datetime:
    """Formate datetime object with end of date time from date object."""
    return datetime.datetime.combine(start_at, datetime.time.max, tzinfo=get_server_timezone())


def convert_from_naive_moscow_datetime_to_utc_timezone(
    *, naive_moscow_datetime: datetime.datetime
) -> datetime.datetime:
    moscow_tz = get_moscow_timezone()
    moscow_date_time = naive_moscow_datetime.replace(tzinfo=moscow_tz)
    return moscow_date_time.astimezone(ZoneInfo("UTC"))


def timer(func: typing.Callable) -> typing.Callable:
    @wraps(func)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        duration_str = str(datetime.timedelta(seconds=duration))
        logger.info(f"Функция '{func.__name__}' выполнилась за {duration_str}")
        return result

    return wrapper


def round_time_to_nearest_half_hour(*, date_time: datetime.datetime) -> datetime.datetime:
    """Округлить время до ближайшего получаса"""
    minutes = date_time.minute
    if minutes < QUARTER_OF_HOUR_IN_MINUTES:
        delta = datetime.timedelta(minutes=minutes, seconds=date_time.second, microseconds=date_time.microsecond)
        return date_time - delta
    if QUARTER_OF_HOUR_IN_MINUTES <= minutes < 3 * QUARTER_OF_HOUR_IN_MINUTES:
        delta = datetime.timedelta(
            minutes=minutes - HALF_OF_HOUR_IN_MINUTES, seconds=date_time.second, microseconds=date_time.microsecond
        )
        return date_time - delta
    delta = datetime.timedelta(
        minutes=HOUR_IN_MINUTES - minutes, seconds=-date_time.second, microseconds=-date_time.microsecond
    )
    return date_time + delta


def datetime_interval__in_available_intervals(
    *, available_intervals: list[TimeIntervalDto] | None, checking_interval: TimeIntervalDto
) -> bool:
    if not available_intervals:
        return False
    for interval in available_intervals:
        if checking_interval.start_at >= interval.start_at and checking_interval.end_at <= interval.end_at:
            return True
    return False

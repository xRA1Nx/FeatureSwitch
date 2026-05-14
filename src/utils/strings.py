from __future__ import annotations

from pydantic.networks import validate_email
from pydantic_core import PydanticCustomError

from src.apps.common.exceptions import BusinessLogicException
from src.apps.feature_flag.logic.interactors.feature_flag import logger


def ensure_valid_email(*, email: str, should_raise_exception: bool = True) -> bool:
    """
    Проверяет, является ли строка валидным email адресом.
    Возвращает True или False.
    """
    try:
        validate_email(email)
    except PydanticCustomError:
        error_message = f'Email = "{email} не корректен!"'
        logger.error(error_message)
        if should_raise_exception:
            raise BusinessLogicException(error_message)
        return False
    else:
        return True

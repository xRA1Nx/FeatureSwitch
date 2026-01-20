from __future__ import annotations

from fastapi import HTTPException


class BusinessLogicException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=420, detail=detail)


class RequestException(BusinessLogicException):
    pass


class ConfigurationsException(BusinessLogicException):
    pass


class NotImplementLogicException(BusinessLogicException):
    pass

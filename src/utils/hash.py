from __future__ import annotations

import typing


def convert_to_hashtable_value(val: typing.Any) -> typing.Any:
    if hasattr(val, "to_pydantic"):
        return val.to_pydantic().dict()
    if hasattr(val, "dict"):
        return val.dict()
    return val

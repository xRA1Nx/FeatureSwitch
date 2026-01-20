from __future__ import annotations

import typing

from polyfactory.factories.pydantic_factory import ModelFactory


T = typing.TypeVar("T")


class orderless(list):  # noqa: N801
    def __eq__(self, other: object) -> bool:
        """
        Costly orderless comparison of elements in two iterables.
        Just like `set(a) == set(b)`, but does not require hashing implemented.
        """
        if not isinstance(other, typing.Iterable):
            return NotImplemented

        reference = list(other)

        if len(reference) != len(self):
            return False

        for item in self:
            try:
                reference.remove(item)
            except ValueError:
                return False

        return True

    def __ne__(self, other: object) -> bool:
        """
        __ne__ is inherited from superclass,
        hence its behaviour would have been inconsistent with custom __eq__.
        """
        return not (self == other)


class SessionHolder:
    session = None

    @classmethod
    def set_session(cls, session):
        cls.session = session


class AsyncSessionMixin:
    @staticmethod
    def session():
        return SessionHolder.session


class BaseDtoFactory(ModelFactory, typing.Generic[T]):
    __is_base_factory__ = True
    __check_model__ = True

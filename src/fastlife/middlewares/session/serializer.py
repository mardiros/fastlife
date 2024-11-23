"""Serialize session."""

import abc
from collections.abc import Mapping
from typing import Any


class AbsractSessionSerializer(abc.ABC):
    """Session serializer base class"""

    @abc.abstractmethod
    def __init__(self, secret_key: str, max_age: int) -> None: ...

    @abc.abstractmethod
    def serialize(self, data: Mapping[str, Any]) -> bytes:
        """Serialize the session content to bytes in order to be saved."""
        ...

    @abc.abstractmethod
    def deserialize(self, data: bytes) -> tuple[Mapping[str, Any], bool]:
        """Derialize the session raw bytes content and return it as a mapping."""
        ...

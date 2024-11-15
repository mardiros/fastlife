"""Types that are serialized over HTTP and forms."""

from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic.networks import EmailStr

Builtins = str | int | str | float | Decimal | UUID | EmailStr
"""Builtins types."""


AnyLiteral = Any
"""
Something like Literal[...] or Literal[...] which does not exists
or Idon't know where it is hidden.
"""

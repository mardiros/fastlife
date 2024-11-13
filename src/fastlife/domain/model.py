from decimal import Decimal
import secrets
from uuid import UUID

from pydantic import BaseModel


Builtins = str | int | str | float | Decimal | UUID


def create_csrf_token() -> str:
    """A helper that create a csrf token."""
    return secrets.token_urlsafe(5)


class CSRFToken(BaseModel):
    name: str
    value: str

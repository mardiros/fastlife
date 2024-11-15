"""Models relative to the security."""

import secrets

from pydantic import BaseModel


def create_csrf_token() -> str:
    """A helper that create a csrf token."""
    return secrets.token_urlsafe(5)


class CSRFToken(BaseModel):
    """Represent the CSRF Token"""

    name: str
    """Name of the token while serialized."""
    value: str
    """Value that must match between parts, cookie and posted form."""

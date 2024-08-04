"""
Prevents CSRF attack using cookie and html hidden field comparaison.

Fast life did not reinvent the wheel on CSRF Protection. It use the good old method.
"""
import secrets
from typing import TYPE_CHECKING, Any, Callable, Coroutine

from fastapi import Request

if TYPE_CHECKING:
    from fastlife.configurator.registry import Registry  # coverage: ignore


class CSRFAttack(Exception):
    """
    An exception raised if the cookie and the csrf token hidden field did not match.
    """


def create_csrf_token() -> str:
    """A helper that create a csrf token."""
    return secrets.token_urlsafe(5)


def check_csrf(registry: "Registry") -> Callable[[Request], Coroutine[Any, Any, bool]]:
    """
    A global application dependency, that is always active.

    If you don't want csrf token, its simple don't use the
    application/x-www-form-urlencoded on a POST method.
    """

    async def check_csrf(request: Request) -> bool:
        if (
            request.method != "POST"
            or request.headers.get("content-type")
            != "application/x-www-form-urlencoded"
        ):
            return True

        cookie = request.cookies.get(registry.settings.csrf_token_name)
        if not cookie:
            raise CSRFAttack("CSRF token did not match")

        form_data = await request.form()
        value = form_data.get(registry.settings.csrf_token_name)
        if value != cookie:
            raise CSRFAttack("CSRF token did not match")

        return True

    return check_csrf

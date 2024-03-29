import secrets
from typing import TYPE_CHECKING, Any, Callable, Coroutine

from fastapi import Request

if TYPE_CHECKING:
    from fastlife.configurator.registry import Registry  # coverage: ignore


class CSRFAttack(Exception):
    ...


def create_csrf_token() -> str:
    return secrets.token_urlsafe(5)


def check_csrf(registry: "Registry") -> Callable[[Request], Coroutine[Any, Any, bool]]:
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

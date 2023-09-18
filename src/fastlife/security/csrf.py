import secrets

from fastapi import Request

CSRF_TOKEN_NAME = "csrf_token"


class CSRFAttack(Exception):
    ...


def create_csrf_token() -> str:
    return secrets.token_urlsafe(5)


async def check_csrf(request: Request) -> bool:
    if (
        request.method != "POST"
        or request.headers.get("content-type") != "application/x-www-form-urlencoded"
    ):
        return True

    cookie = request.cookies.get(CSRF_TOKEN_NAME)
    if not cookie:
        raise CSRFAttack("CSRF token did not match")

    form_data = await request.form()
    value = form_data.get(CSRF_TOKEN_NAME)
    if value != cookie:
        raise CSRFAttack("CSRF token did not match")

    return True

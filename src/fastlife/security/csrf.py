"""
Prevents CSRF attack using cookie and html hidden field comparison.

Fast life did not reinvent the wheel on CSRF Protection.

It use the good old method. A CSRF token is saved in a cookie.
Forms post the CSRF token, and the token in the cookies and the form must match
to process the request, otherwise an exception
{class}`fastlife.security.csrf.CSRFAttack` is raised.

The cookie named is configurabllefia the settings
:attr:`fastlife.config.settings.Settings.csrf_token_name`

While using the `<Form/>` JinjaX tag, the csrf token is always sent.

The cookie is always set when you render any template. At the moment, there is
no way to prevent to set the cookie in the request.

"""

import secrets
from typing import Any, Callable, Coroutine

from fastlife.request import Request


class CSRFAttack(Exception):
    """
    An exception raised if the cookie and the csrf token hidden field did not match.
    """


def create_csrf_token() -> str:
    """A helper that create a csrf token."""
    return secrets.token_urlsafe(5)


def check_csrf() -> Callable[[Request], Coroutine[Any, Any, bool]]:
    """
    A global application dependency, that is always active.

    If you don't want csrf token, its simple: don't use the
    application/x-www-form-urlencoded on a POST method.

    For security reason, there it no other options to disable this policy.

    :raises: {class}`.CSRFAttack` if the cookie and the csrf
        posted in the form does not match.
    """

    async def check_csrf(request: Request) -> bool:
        if (
            request.method != "POST"
            or request.headers.get("content-type")
            != "application/x-www-form-urlencoded"
        ):
            return True
        csrf_token_name = request.registry.settings.csrf_token_name

        cookie = request.cookies.get(csrf_token_name)
        if not cookie:
            raise CSRFAttack("CSRF token did not match")

        form_data = await request.form()
        value = form_data.get(csrf_token_name)
        if value != cookie:
            raise CSRFAttack("CSRF token did not match")

        return True

    return check_csrf

"""
Prevents CSRF attack using cookie and html hidden field comparison.

Fast life did not reinvent the wheel on CSRF Protection.

It use the good old method. A CSRF token is saved in a cookie.
Forms post the CSRF token, and the token in the cookies and the form must match
to process the request, otherwise an exception
{class}`fastlife.service.csrf.CSRFAttack` is raised.

The cookie named is configurabllefia the settings
:attr:`fastlife.config.settings.Settings.csrf_token_name`

While using the `<Form/>` JinjaX tag, the csrf token is always sent.

The cookie is always set when you render any template. At the moment, there is
no way to prevent to set the cookie in the request.

"""

from collections.abc import Callable, Coroutine
from typing import Any

from fastlife.adapters.fastapi.request import Request


class CSRFAttack(Exception):
    """
    An exception raised if the cookie and the csrf token hidden field did not match.
    """


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

        token = request.csrf_token
        form_data = await request.form()
        value = form_data.get(token.name)
        if value != token.value:
            raise CSRFAttack("CSRF token did not match")

        return True

    return check_csrf

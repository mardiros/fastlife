from typing import Annotated

from fastapi import Depends, Request, Response

from fastlife import Configurator, configure
from tests.fastlife_app.security import AuthenticatedUser, authenticated_user


class MyException(Exception):
    """Custom exception"""


def my_handler(request: Request, exc: MyException) -> Response:
    return Response("It's a trap")


async def failed(
    user: Annotated[AuthenticatedUser, Depends(authenticated_user)],
) -> Response:
    raise MyException


@configure
def includeme(config: Configurator):
    config.add_exception_handler(MyException, my_handler)
    config.add_route("failed", "/failed", failed)

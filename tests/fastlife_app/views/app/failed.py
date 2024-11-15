from fastapi import Request, Response

from fastlife.config.exceptions import exception_handler
from fastlife.config.views import view_config
from fastlife.domain.model.template import JinjaXTemplate


class MyGoodException(Exception):
    """Custom exception to test the exception handler rendered with a template."""


class MyBadException(Exception):
    """Custom exception that will finally raised a runtime error."""


class MyUglyException(Exception):
    """Custom exception that return a raw response directly. not that ugly, just fun."""


class YourFault(Exception):
    """Custom exception for 4xx error example."""

    def __init__(self, message: str) -> None:
        self.message = message


class Error500(JinjaXTemplate):
    template = """<E500 :message="message" />"""
    message: str


class Error422(JinjaXTemplate):
    template = """<E422 :message="message" />"""
    message: str


@exception_handler(MyGoodException)
def my_good_handler(request: Request, exc: MyGoodException) -> Error500:
    return Error500(message="It's a trap")


@exception_handler(MyUglyException, status_code=500)
def my_ugly_handler(request: Request, exc: MyUglyException) -> Response:
    return Response(
        "It's a trap", headers={"Content-Type": "text/plain"}, status_code=400
    )


@exception_handler(YourFault, status_code=422)
def your_fault_handler(request: Request, exc: YourFault) -> Error422:
    return Error422(message=exc.message)


@view_config("failed", "/failed-good")
async def failed() -> Response:
    raise MyGoodException


@view_config("failed", "/failed-ugly")
async def failed_ugly() -> Response:
    raise MyUglyException


@view_config("failed", "/your-fault")
async def your_fault() -> Response:
    raise YourFault("Invalid Parameter")

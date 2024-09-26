import textwrap

from pydantic import BaseModel

from fastlife import Configurator, configure


class Info(BaseModel):
    version: str
    build: str


async def info() -> Info:
    return Info(version="1.0", build="856f241")


@configure
def includeme(config: Configurator):
    config.set_api_documentation_info(
        "Dummy API",
        "4.2",
        textwrap.dedent(
            """
            In a unit test suite, a dummy is a simple placeholder object used to
            satisfy the parameter requirements of a method or function but isn't
            actively used in the test.

            Its primary role is to avoid null or undefined values when a method
            expects an argument, but the argument itself is irrelevant to the
            test being performed.

            For example, if a function requires multiple parameters and you're
            only interested in testing the behavior of one of them, you
            can use a **dummy** for the others to focus on the aspect you're testing.

            Unlike **mocks** or **stubs**, a **dummy doesn't have any behavior
            or interactions** it's just there to fulfill the method's signature.
            """
        ),
        "API for dummies",
    )
    config.add_api_route(
        "home",
        "",
        info,
        methods=["GET"],
        summary="Retrieve Build Information",
        description="Return application build information",
        response_description="Build Info",
        tags=["monitoring"],
    )

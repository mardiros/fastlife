from pydantic import BaseModel

from fastlife import Configurator, configure


class Info(BaseModel):
    version: str
    build: str


async def info() -> Info:
    return Info(version="1.0", build="856f241")


@configure
def includeme(config: Configurator):
    config.set_api_documentation_info("Dummy API", "4.2")
    config.add_api_route(
        "home",
        "/api",
        info,
        methods=["GET"],
        summary="Retrieve Build Information",
        description="Return application build information",
        response_description="Build Info",
        tags=["monitoring"],
    )

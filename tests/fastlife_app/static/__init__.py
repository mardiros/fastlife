from pathlib import Path

from fastapi import Response
from starlette.responses import FileResponse

from fastlife.config import Configurator, configure

static_dir = Path(__file__).parent
favicon_path = Path(__file__).parent / "favicon.ico"


async def favicon() -> Response:
    return FileResponse(favicon_path)


@configure
def includeme(config: Configurator):
    config.add_route("favicon", "/favicon.ico", favicon, methods=["GET"])
    config.add_static_route("/static/css", static_dir / "css", name="static")

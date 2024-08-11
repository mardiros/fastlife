import datetime
from datetime import timedelta
from importlib import metadata, util
from pathlib import Path

from fastapi import HTTPException, Response
from fastapi.responses import FileResponse

from fastlife import Configurator, configure

package_name = "fontawesomefree"


@configure
def includeme(config: Configurator) -> None:
    try:
        version = metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return

    spec = util.find_spec(package_name)
    if spec is None or spec.origin is None:
        return
    fontawesome_path = Path(spec.origin).parent / "static" / "fontawesomefree"

    config.add_static_route(
        f"/static/components/font-awesome/{version}",
        directory=fontawesome_path,
    )

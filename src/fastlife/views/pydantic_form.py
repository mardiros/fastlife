from typing import Optional

from fastapi import Query, Response

from fastlife import Configurator, configure
from fastlife.configurator.registry import Registry
from fastlife.shared_utils.resolver import resolve_extended


async def show_widget(
    typ: str,
    reg: Registry,
    name: Optional[str] = Query(...),
    token: Optional[str] = Query(...),
    removable: bool = Query(False),
) -> Response:
    model_cls = resolve_extended(typ)
    data = await reg.renderer.pydantic_form(model_cls, None, name, token, removable)
    return Response(data, headers={"Content-Type": "text/html"})


@configure
def includeme(config: Configurator) -> None:
    route_prefix = config.registry.settings.fastlife_route_prefix
    config.add_route(
        "fl-pydantic-form-widget",
        f"{route_prefix}/pydantic-form/widgets/{{typ}}",
        show_widget,
        methods=["GET"],
    )

from typing import Optional

from fastapi import Query, Request, Response
from pydantic.fields import FieldInfo

from fastlife import Configurator, configure
from fastlife.configurator.registry import Registry
from fastlife.shared_utils.resolver import resolve_extended


async def show_widget(
    typ: str,
    reg: Registry,
    request: Request,
    title: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    token: Optional[str] = Query(None),
    removable: bool = Query(False),
) -> Response:
    model_cls = resolve_extended(typ)
    field = None
    if title:
        field = FieldInfo(title=title)
    data = reg.renderer(request).pydantic_form_field(
        model=model_cls,
        name=name,
        token=token,
        removable=removable,
        field=field,
    )
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

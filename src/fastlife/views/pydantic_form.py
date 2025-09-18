"""
Views for pydantic form.

Pydantic form generate form that may contains fields that requires some ajax query.
"""

from typing import Literal

from fastapi import Query
from pydantic.fields import FieldInfo

from fastlife import Configurator, Request, Response, configure
from fastlife.shared_utils.resolver import resolve_extended


async def show_widget(
    typ: str,
    request: Request,
    title: str | None = Query(None),
    name: str | None = Query(None),
    token: str | None = Query(None),
    format: Literal["jinjax", "xcomponent"] | str = Query("jinjax"),
    removable: bool = Query(False),
) -> Response:
    """
    This views is used by pydantic_form to generate a nested field asynchronously.
    """
    model_cls = resolve_extended(typ)
    field = None
    if title:
        field = FieldInfo(title=title)

    if format == "jinjax":
        # XXX
        format = request.registry.settings.jinjax_file_ext
    rndr = request.registry.get_renderer(f".{format}")(request)
    lczr = request.registry.localizer(request.locale_name)
    rndr.globals.update({"request": request, **lczr.as_dict()})
    data = rndr.pydantic_form_field(
        model=model_cls,  # type: ignore
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

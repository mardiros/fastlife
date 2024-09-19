from enum import Enum
from typing import Any, Callable

import venusian
from fastapi.types import IncEx

from .configurator import VENUSIAN_CATEGORY, Configurator


def view_config(
    name: str,
    path: str,
    *,
    permission: str | None = None,
    status_code: int | None = None,
    tags: list[str | Enum] | None = None,
    summary: str | None = None,
    description: str | None = None,
    response_description: str = "Successful Response",
    # responses: Dict[Union[int, str], Dict[str, Any]] | None = None,
    deprecated: bool | None = None,
    methods: list[str] | None = None,
    operation_id: str | None = None,
    # response_model: Any = Default(None),
    response_model_include: IncEx | None = None,
    response_model_exclude: IncEx | None = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    # response_class: Union[Type[Response], DefaultPlaceholder] = Default(
    #     HTMLResponse
    # ),
    openapi_extra: dict[str, Any] | None = None,
) -> Callable[..., Any]:
    view_name = name

    def configure(
        wrapped: Callable[..., Any],
    ) -> Callable[..., Any]:

        def callback(
            scanner: venusian.Scanner, name: str, ob: Callable[..., Any]
        ) -> None:
            if not hasattr(scanner, "fastlife"):
                return
            config: Configurator = getattr(scanner, VENUSIAN_CATEGORY)
            config.add_api_route(
                name=view_name,
                path=path,
                endpoint=ob,
                permission=permission,
                status_code=status_code,
                tags=tags,
                summary=summary,
                description=description,
                response_description=response_description,
                deprecated=deprecated,
                methods=methods,
                operation_id=operation_id,
                response_model_include=response_model_include,
                response_model_exclude=response_model_exclude,
                response_model_by_alias=response_model_by_alias,
                response_model_exclude_unset=response_model_exclude_unset,
                response_model_exclude_defaults=response_model_exclude_defaults,
                response_model_exclude_none=response_model_exclude_none,
                include_in_schema=include_in_schema,
                openapi_extra=openapi_extra,
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure

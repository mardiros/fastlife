from typing import Any, Callable

import venusian
from fastapi.types import IncEx

from .configurator import VENUSIAN_CATEGORY, Configurator


def resource(
    name: str,
    *,
    path: str | None = None,
    collection_path: str | None = None,
    description: str | None = None,
) -> Callable[..., Any]:
    tag = name

    def configure(
        wrapped: Callable[..., Any],
    ) -> Callable[..., Any]:
        """
        Decorator used to attach route in a submodule while using the configurator.include.
        """

        def callback(scanner: venusian.Scanner, name: str, ob: type[Any]) -> None:
            if not hasattr(scanner, VENUSIAN_CATEGORY):
                return

            config: Configurator = getattr(scanner, VENUSIAN_CATEGORY)

            api = ob()

            def bind_config(
                bind_config: Configurator,
                method: str,
                bind_path: str | None,
                endpoint: Any,
            ):
                if bind_path is None:
                    prefix = "collection_" if method.startswith("collection_") else ""
                    raise RuntimeError(f"{prefix}path not set on resource {tag}")

                bind_config.add_api_route(
                    name=f"{method}_{tag}",
                    path=bind_path,
                    endpoint=endpoint,
                    tags=[tag],
                    methods=[method.split("_").pop()],
                    permission=getattr(endpoint, "permission"),
                    status_code=getattr(endpoint, "status_code"),
                    summary=getattr(endpoint, "summary"),
                    description=getattr(endpoint, "description"),
                    response_description=getattr(endpoint, "response_description"),
                    deprecated=getattr(endpoint, "deprecated"),
                    operation_id=getattr(endpoint, "operation_id"),
                    response_model_include=getattr(endpoint, "response_model_include"),
                    response_model_exclude=getattr(endpoint, "response_model_exclude"),
                    response_model_by_alias=getattr(
                        endpoint, "response_model_by_alias"
                    ),
                    response_model_exclude_unset=getattr(
                        endpoint, "response_model_exclude_unset"
                    ),
                    response_model_exclude_defaults=getattr(
                        endpoint, "response_model_exclude_defaults"
                    ),
                    response_model_exclude_none=getattr(
                        endpoint, "response_model_exclude_none"
                    ),
                    include_in_schema=getattr(endpoint, "include_in_schema"),
                    openapi_extra=getattr(endpoint, "openapi_extra"),
                )

            for method in dir(ob):
                match method:
                    case (
                        "collection_get"
                        | "collection_post"
                        | "collection_put"
                        | "collection_patch"
                        | "collection_delete"
                    ):
                        bind_config(
                            config, method, collection_path, getattr(api, method)
                        )
                    case "get" | "post" | "put" | "patch" | "delete":
                        bind_config(config, method, path, getattr(api, method))
                    case _:
                        ...

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure


class resource_view:
    def __init__(
        self,
        permission: str | None = None,
        status_code: int | None = None,
        summary: str | None = None,
        description: str | None = None,
        response_description: str = "Successful Response",
        deprecated: bool | None = None,
        methods: list[str] | None = None,
        operation_id: str | None = None,
        response_model_include: IncEx | None = None,
        response_model_exclude: IncEx | None = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        openapi_extra: dict[str, Any] | None = None,
    ) -> None:
        self.permission = permission
        self.status_code = status_code
        self.summary = summary
        self.description = description
        self.response_description = response_description
        self.deprecated = deprecated
        self.methods = methods
        self.operation_id = operation_id
        self.response_model_include = response_model_include
        self.response_model_exclude = response_model_exclude
        self.response_model_by_alias = response_model_by_alias
        self.response_model_exclude_unset = response_model_exclude_unset
        self.response_model_exclude_defaults = response_model_exclude_defaults
        self.response_model_exclude_none = response_model_exclude_none
        self.include_in_schema = include_in_schema
        self.openapi_extra = openapi_extra

    def __call__(self, fn: Any) -> Any:
        fn.permission = self.permission
        fn.status_code = self.status_code
        fn.summary = self.summary
        fn.description = self.description
        fn.response_description = self.response_description
        fn.deprecated = self.deprecated
        fn.methods = self.methods
        fn.operation_id = self.operation_id
        fn.response_model_include = self.response_model_include
        fn.response_model_exclude = self.response_model_exclude
        fn.response_model_by_alias = self.response_model_by_alias
        fn.response_model_exclude_unset = self.response_model_exclude_unset
        fn.response_model_exclude_defaults = self.response_model_exclude_defaults
        fn.response_model_exclude_none = self.response_model_exclude_none
        fn.include_in_schema = self.include_in_schema
        fn.openapi_extra = self.openapi_extra
        return fn

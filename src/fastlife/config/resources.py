"""
API Resources declaration using a decorator.


```{literalinclude} ../../../../tests/fastlife_app/views/api/foos.py

```

"""

from collections.abc import Callable
from typing import Any

import venusian
from fastapi.types import IncEx

from fastlife.config.openapiextra import ExternalDocs

from .configurator import (
    VENUSIAN_CATEGORY,
    ConfigurationError,
    Configurator,
    OpenApiTag,
)


def resource(
    name: str,
    *,
    path: str | None = None,
    collection_path: str | None = None,
    description: str | None = None,
    external_docs: ExternalDocs | None = None,
) -> Callable[..., Any]:
    """
    A decorator to build an OpenAPI set of api grouped under a tag.

    This approach makes the resource the umbrella for all API methods that
    modify resources of that type, covering operations on both collections and
    individual items.

    The typical set of api route to manage resources is:

      * `POST /items`: a POST on a `collection_path` that create an item
      * `GET /items?filters=...&page=...`: a GET on a `collection_path` to list or
        even search items. Usually it returns partial item fields.
      * `GET /items/{id}`: Return the item with all its fields.
      * `PATCH /items/{id}`: An update of a single item on the resource `path`.
      * `DELETE /items/{id}`: Remove a single item from the collection on the `path`.

    You may implement more methods: `collection_get`, `collection_post`,
    `collection_put`, `collection_patch`, `collection_delete`, `collection_head`,
    `collection_options`, `get`, `post`, `put`, `patch`, `delete`, `head`, `options`
    will autmatically be bound to verb collection path or path.

    Note that there is no abstract class that declare this method, this is done by
    introspection while returning the configuration method
    {meth}`fastlife.config.configurator.GenericConfigurator.include`
    """
    tag = name

    def configure(
        wrapped: Callable[..., Any],
    ) -> Callable[..., Any]:
        def callback(scanner: venusian.Scanner, name: str, ob: type[Any]) -> None:
            if not hasattr(scanner, VENUSIAN_CATEGORY):
                return  # coverage: ignore

            config: Configurator = getattr(scanner, VENUSIAN_CATEGORY)
            if description:
                config.add_openapi_tag(
                    OpenApiTag(
                        name=tag, description=description, externalDocs=external_docs
                    )
                )

            api = ob()

            def bind_config(
                bind_config: Configurator,
                method: str,
                bind_path: str | None,
                endpoint: Any,
            ) -> None:
                if bind_path is None:
                    prefix = "collection_" if method.startswith("collection_") else ""
                    raise ConfigurationError(f"{prefix}path not set on resource {tag}")

                bind_config.add_api_route(
                    name=f"{method}_{tag}",
                    path=bind_path,
                    endpoint=endpoint,
                    tags=[tag],
                    methods=[method.split("_").pop()],
                    permission=endpoint.permission,
                    status_code=endpoint.status_code,
                    summary=endpoint.summary,
                    description=endpoint.description,
                    response_description=endpoint.response_description,
                    deprecated=endpoint.deprecated,
                    operation_id=endpoint.operation_id,
                    response_model_include=endpoint.response_model_include,
                    response_model_exclude=endpoint.response_model_exclude,
                    response_model_by_alias=endpoint.response_model_by_alias,
                    response_model_exclude_unset=endpoint.response_model_exclude_unset,
                    response_model_exclude_defaults=endpoint.response_model_exclude_defaults,
                    response_model_exclude_none=endpoint.response_model_exclude_none,
                    include_in_schema=endpoint.include_in_schema,
                    openapi_extra=endpoint.openapi_extra,
                )

            for method in dir(ob):
                match method:
                    case (
                        "collection_get"
                        | "collection_post"
                        | "collection_put"
                        | "collection_patch"
                        | "collection_delete"
                        | "collection_head"
                        | "collection_options"
                    ):
                        bind_config(
                            config, method, collection_path, getattr(api, method)
                        )
                    case (
                        "get" | "post" | "put" | "patch" | "delete" | "head" | "options"
                    ):
                        bind_config(config, method, path, getattr(api, method))
                    case _:
                        ...

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return configure


def resource_view(
    *,
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
) -> Callable[..., Any]:
    """ "
    Decorator to use on a method of a class decorated with {func}`resource` in order
    to add OpenAPI information.

    This decorator has an effect if the decoratated method is named `collection_get`,
    `collection_post`, `collection_put`, `collection_patch`, `collection_delete`,
    `collection_head`, `collection_options`, `get`, `post`, `put`, `patch`, `delete`,
    `head` or `options`.

    :param permission: a permission to validate by the security policy.
    :param status_code: returned status_code
    :param summary: OpenAPI summary for the route.
    :param description:OpenAPI description for the route.
    :param response_description: OpenAPI description for the response.
    :param operation_id: OpenAPI optional unique string used to identify an
        operation.
    :param tags: OpenAPI tags for the route.
    :param deprecated: OpenAPI deprecated annotation for the route.
    :param openapi_extra: OpenAPI documentation extra fields.
    :param include_in_schema: Expose or not the route in the OpenAPI schema and
    documentation.

    :param response_model_include: customize fields list to include in repsonse.
    :param response_model_exclude: customize fields list to exclude in repsonse.
    :param response_model_by_alias: serialize fields by alias or by name if False.
    :param response_model_exclude_unset: exclude fields that are not explicitly
        set in response.
    :param response_model_exclude_defaults: exclude default value of response
        fields.
    :param response_model_exclude_none: exclude fields instead of serialize to
        null value.
    """

    def wrapped(fn: Any) -> Any:
        fn.permission = permission
        fn.status_code = status_code
        fn.summary = summary
        fn.description = description
        fn.response_description = response_description
        fn.deprecated = deprecated
        fn.methods = methods
        fn.operation_id = operation_id
        fn.response_model_include = response_model_include
        fn.response_model_exclude = response_model_exclude
        fn.response_model_by_alias = response_model_by_alias
        fn.response_model_exclude_unset = response_model_exclude_unset
        fn.response_model_exclude_defaults = response_model_exclude_defaults
        fn.response_model_exclude_none = response_model_exclude_none
        fn.include_in_schema = include_in_schema
        fn.openapi_extra = openapi_extra
        return fn

    return wrapped

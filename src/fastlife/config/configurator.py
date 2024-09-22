"""
The configurator registers routes in a FastAPI application while
adding support for dependency injection during the configuration phase.

FastAPI does not provide any built-in support for dependency injection
during the configuration phase.
Instead, it only resolves dependencies at request time, ensuring they
are dynamically handled per request.

The configurator is designed to handle the setup during the configuration
phase.
"""

import importlib
import inspect
import logging
from collections.abc import Mapping
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Annotated, Any, Callable, Self, Tuple, Type, cast

import venusian
from fastapi import Depends, FastAPI
from fastapi import Request as BaseRequest
from fastapi import Response
from fastapi.params import Depends as DependsType
from fastapi.staticfiles import StaticFiles
from fastapi.types import IncEx
from pydantic import BaseModel, Field

from fastlife.middlewares.base import AbstractMiddleware
from fastlife.request.request import Request
from fastlife.routing.route import Route
from fastlife.routing.router import Router
from fastlife.security.csrf import check_csrf
from fastlife.shared_utils.resolver import resolve

from .settings import Settings

if TYPE_CHECKING:
    from .registry import AppRegistry  # coverage: ignore

log = logging.getLogger(__name__)
VENUSIAN_CATEGORY = "fastlife"


class ConfigurationError(Exception):
    """
    Error raised during configuration, to avoid errors at runtime.
    """


class ExternalDocs(BaseModel):
    """OpenAPI externalDocs object."""

    description: str
    """link's description."""
    url: str
    """link's URL."""


class OpenApiTag(BaseModel):
    """OpenAPI tag object."""

    name: str
    """name of the tag."""
    description: str
    """explanation of the tag."""
    external_docs: ExternalDocs | None = Field(alias="externalDocs", default=None)
    """external link to the doc."""


class Configurator:
    """
    Configure and build an application.

    Initialize the app from the settings.
    """

    registry: "AppRegistry"

    def __init__(self, settings: Settings) -> None:
        """
        :param settings: application settings.
        """
        registry_cls = resolve(settings.registry_class)
        self.registry = registry_cls(settings)
        Route._registry = self.registry  # type: ignore

        self.middlewares: list[Tuple[Type[AbstractMiddleware], Any]] = []
        self.exception_handlers: list[Tuple[int | Type[Exception], Any]] = []
        self.mounts: list[Tuple[str, Path, str]] = []
        self.tags: dict[str, OpenApiTag] = {}

        self.api_title = "OpenAPI"
        self.api_version = "v1"
        self.api_description: str = ""
        self.api_summary: str | None = None

        self.router = Router()
        self.scanner = venusian.Scanner(fastlife=self)
        self.include("fastlife.views")
        self.include("fastlife.middlewares")

    def build_asgi_app(self) -> FastAPI:
        """
        Build the app after configuration in order to start after beeing configured.

        :return: FastAPI application.
        """
        _app = FastAPI(
            title=self.api_title,
            version=self.api_version,
            description=self.api_description,
            summary=self.api_summary,
            dependencies=[Depends(check_csrf())],
            docs_url=self.registry.settings.api_swagger_ui_url,
            redoc_url=self.registry.settings.api_redocs_url,
            openapi_tags=[tag.model_dump(by_alias=True) for tag in self.tags.values()]
            if self.tags
            else None,
        )
        _app.router.route_class = Route
        for _route in self.router.routes:
            route = cast(Route, _route)
            _app.router.add_api_route(
                path=route.path,
                endpoint=route.endpoint,
                response_model=route.response_model,
                status_code=route.status_code,
                tags=route.tags,
                dependencies=route.dependencies,
                summary=route.summary,
                description=route.description,
                response_description=route.response_description,
                deprecated=route.deprecated,
                methods=route.methods,
                operation_id=route.operation_id,
                response_model_include=route.response_model_include,
                response_model_exclude=route.response_model_exclude,
                response_model_by_alias=route.response_model_by_alias,
                response_model_exclude_unset=route.response_model_exclude_unset,
                response_model_exclude_defaults=route.response_model_exclude_defaults,
                response_model_exclude_none=route.response_model_exclude_none,
                include_in_schema=route.include_in_schema,
                name=route.name,
                openapi_extra=route.openapi_extra,
            )

        for middleware_class, options in self.middlewares:
            _app.add_middleware(middleware_class, **options)  # type: ignore

        for status_code_or_exc, exception_handler in self.exception_handlers:
            _app.add_exception_handler(status_code_or_exc, exception_handler)

        for route_path, directory, name in self.mounts:
            _app.mount(route_path, StaticFiles(directory=directory), name=name)
        return _app

    def include(self, module: str | ModuleType) -> Self:
        """
        Include a module in order to load its configuration.

        It will load and include all the submodule as well.

        Here is an example.

        ```python
        from fastlife import Configurator, configure

        def home() -> dict[str, str]:
            return {"hello": "world"}

        @configure
        def includeme(config: Configurator) -> None:
            config.add_route("home", "/", home)
        ```

        :param module: a module to include.
        """
        if isinstance(module, str):
            package = None
            if module.startswith("."):
                caller_module = inspect.getmodule(inspect.stack()[1][0])
                package = caller_module.__name__ if caller_module else "__main__"

            module = importlib.import_module(module, package)
        self.scanner.scan(module, categories=[VENUSIAN_CATEGORY])  # type: ignore
        return self

    def set_api_documentation_info(
        self,
        title: str,
        version: str,
        description: str,
        summary: str | None = None,
    ) -> Self:
        """
        Set your api documentation title for application that expose an API.

        :param title: OpenAPI documentation title
        :param version: OpenAPI api version
        :param description: OpenAPI documentation description
        :param summary: OpenAPI documentation summary
        """
        self.api_title = title
        self.api_version = version
        self.api_description = description
        self.api_summary = summary
        return self

    def add_open_tag(self, tag: OpenApiTag) -> Self:
        """Register a tag description in the documentation."""
        if tag.name in self.tags:
            raise ConfigurationError(f"Tag {tag.name} can't be registered twice.")
        self.tags[tag.name] = tag
        return self

    def add_middleware(
        self, middleware_class: Type[AbstractMiddleware], **options: Any
    ) -> Self:
        """
        Add a starlette middleware to the FastAPI app.
        """
        self.middlewares.append((middleware_class, options))
        return self

    def add_api_route(
        self,
        name: str,
        path: str,
        endpoint: Callable[..., Any],
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
        # generate_unique_id_function: Callable[[APIRoute], str] = Default(
        #     generate_unique_id
        # ),
    ) -> Self:
        """
        Add an API route to the app.

        Fastlife does not use a decorator to attach routes, instead the decorator
        :func:`fastlife.config.configurator.configure` has to be used to
        inject routes inside a method and call the add_route method.

        This route has to be used to add API Route, by API, to expose it in the
        documentation.

        To add a route that serve HTML user the method {meth}`Configurator.add_route`

        :param name: name of the route, used to build route from the helper
            :meth:`fastlife.request.request.Request.url_for` in order to create links.
        :param path: path of the route, use `{curly_brace}` to inject FastAPI Path
            parameters.
        :param endpoint: the function that will reveive the request.
        :param permission: a permission to validate by the
            :attr:`fastlife.config.settings.Settings.check_permission` function.

        :param methods: restrict route to a list of http methods.
        :param description:OpenAPI description for the route.
        :param summary: OpenAPI summary for the route.
        :param response_description: OpenAPI description for the response.
        :param operation_id: OpenAPI optional unique string used to identify an
            operation.
        :param tags: OpenAPI tags for the route.
        :param deprecated: OpenAPI deprecated annotation for the route.

        :param response_model_include: customize fields list to include in repsonse.
        :param response_model_exclude: customize fields list to exclude in repsonse.
        :param response_model_by_alias: serialize fields by alias or by name if False.
        :param response_model_exclude_unset: exclude fields that are not explicitly
            set in response.
        :param response_model_exclude_defaults: exclude default value of response
            fields.
        :param response_model_exclude_none: exclude fields instead of serialize to
            null value.
        :param include_in_schema: expose or not the route in the doc.
        :param openapi_extra: open api documentation extra fields.

        :return: the configurator.
        """
        dependencies: list[DependsType] = []
        if permission:
            dependencies.append(Depends(self.registry.check_permission(permission)))

        self.router.add_api_route(
            path,
            endpoint,
            # response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            # responses=responses,
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id or name,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            # response_class=response_class,
            name=name,
            openapi_extra=openapi_extra,
            # generate_unique_id_function=generate_unique_id_function,
        )
        return self

    def add_route(
        self,
        name: str,
        path: str,
        endpoint: Callable[..., Any],
        *,
        permission: str | None = None,
        template: str | None = None,
        status_code: int | None = None,
        methods: list[str] | None = None,
    ) -> Self:
        """
        Add a route to the app.

        Fastlife does not use the FastAPI decorator to attach routes, instead the
        decorator {func}`@configure <fastlife.config.configurator.configure>` has to
        be used to inject routes inside a method and call the add_route method.
        Or the decorator {func}`@view_config <fastlife.config.views.view_config>`
        can decorate view functions.

        :param name: name of the route, used to build route from the helper
            :meth:`fastlife.request.request.Request.url_for` in order to create links.
        :param path: path of the route, use `{curly_brace}` to inject FastAPI Path
            parameters.
        :param endpoint: the function that will reveive the request.
        :param permission: a permission to validate by the
            :attr:`fastlife.config.settings.Settings.check_permission` function.

        :param methods: restrict route to a list of http methods.
        :return: the configurator.
        """
        dependencies: list[DependsType] = []
        if permission:
            dependencies.append(Depends(self.registry.check_permission(permission)))

        if template:

            def render(
                request: Request,
                resp: Annotated[Response | Mapping[str, Any], Depends(endpoint)],
            ) -> Response:
                if isinstance(resp, Response):
                    return resp
                return request.registry.get_renderer(template)(request).render(
                    template,
                    params=resp,
                )

            endpoint = render

        self.router.add_api_route(
            path,
            endpoint,
            status_code=status_code,
            dependencies=dependencies,
            methods=methods,
            include_in_schema=False,
            name=name,
        )
        return self

    def add_static_route(
        self, route_path: str, directory: Path, name: str = "static"
    ) -> Self:
        """
        Mount a directory to an http endpoint.

        :param route_path: the root path for the statics.
        :param directory: the directory on the filesystem where the statics files are.
        :param name: a name for the route in the starlette app.
        :return: the configurator

        """
        self.mounts.append((route_path, directory, name))
        return self

    def add_exception_handler(
        self, status_code_or_exc: int | Type[Exception], handler: Any
    ) -> Self:
        """Add an exception handler the application."""

        def exception_handler(request: BaseRequest, exc: Exception) -> Any:
            req = Request(self.registry, request)
            return handler(req, exc)

        self.exception_handlers.append((status_code_or_exc, exception_handler))
        return self


def configure(
    wrapped: Callable[[Configurator], None],
) -> Callable[[Configurator], None]:
    """
    Decorator used to attach route in a submodule while using the configurator.include.
    """

    def callback(
        scanner: venusian.Scanner, name: str, ob: Callable[[venusian.Scanner], None]
    ) -> None:
        if hasattr(scanner, "fastlife"):
            ob(scanner.fastlife)  # type: ignore

    venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
    return wrapped

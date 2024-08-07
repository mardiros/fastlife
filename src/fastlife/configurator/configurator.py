"""
The configurator is here to register routes in a fastapi app,
with dependency injection.
"""

import importlib
import inspect
import logging
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    List,
    Optional,
    Self,
    Type,
    Union,
)

import venusian  # type: ignore
from fastapi import Depends, FastAPI, Request, Response
from fastapi.params import Depends as DependsType
from fastapi.staticfiles import StaticFiles

from fastlife.configurator.base import AbstractMiddleware
from fastlife.configurator.route_handler import FastlifeRoute
from fastlife.security.csrf import check_csrf

from .route_handler import FastlifeRequest
from .settings import Settings

if TYPE_CHECKING:
    from .registry import AppRegistry  # coverage: ignore

log = logging.getLogger(__name__)
VENUSIAN_CATEGORY = "fastlife"


class Configurator:
    """
    Configure and build an application.

    Initialize the app from the settings.

    :param settings: Application settings.
    """

    registry: "AppRegistry"

    def __init__(self, settings: Settings) -> None:
        from .registry import initialize_registry  # XXX circular import

        self.registry = initialize_registry(settings)
        self._app = FastAPI(
            dependencies=[Depends(check_csrf(self.registry))],
            docs_url=None,
            redoc_url=None,
        )
        FastlifeRoute.registry = self.registry
        self._app.router.route_class = FastlifeRoute
        self.scanner = venusian.Scanner(fastlife=self)
        self.include("fastlife.views")
        self.include("fastlife.middlewares")

    def get_app(self) -> FastAPI:
        """
        Get the app after configuration in order to start after beeing configured.

        :return: FastAPI application
        """
        return self._app

    def include(self, module: str | ModuleType) -> "Configurator":
        """
        Include a module in order to load its views.

        Here is an example.

        ::

            from fastlife import Configurator, configure

            @configure
            def includeme(config: Configurator) -> None:
                config.include(".views")


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

    def add_middleware(
        self, middleware_class: Type[AbstractMiddleware], **options: Any
    ) -> Self:
        """
        Add a starlette middleware to the FastAPI app.
        """
        self._app.add_middleware(middleware_class, **options)  # type: ignore
        return self

    def add_route(
        self,
        name: str,
        path: str,
        endpoint: Callable[..., Coroutine[Any, Any, Response]],
        *,
        permission: str | None = None,
        status_code: int | None = None,
        tags: List[Union[str, Enum]] | None = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        # responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        methods: Optional[List[str]] = None,
        # operation_id: Optional[str] = None,
        # response_model: Any = Default(None),
        # response_model_include: Optional[IncEx] = None,
        # response_model_exclude: Optional[IncEx] = None,
        # response_model_by_alias: bool = True,
        # response_model_exclude_unset: bool = False,
        # response_model_exclude_defaults: bool = False,
        # response_model_exclude_none: bool = False,
        # include_in_schema: bool = True,
        # response_class: Union[Type[Response], DefaultPlaceholder] = Default(
        #     HTMLResponse
        # ),
        # openapi_extra: Optional[Dict[str, Any]] = None,
        # generate_unique_id_function: Callable[[APIRoute], str] = Default(
        #     generate_unique_id
        # ),
    ) -> "Configurator":
        """Add a route to the app."""
        dependencies: List[DependsType] = []
        if permission:
            dependencies.append(Depends(self.registry.check_permission(permission)))

        self._app.add_api_route(
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
            # operation_id=operation_id,
            # response_model_include=response_model_include,
            # response_model_exclude=response_model_exclude,
            # response_model_by_alias=response_model_by_alias,
            # response_model_exclude_unset=response_model_exclude_unset,
            # response_model_exclude_defaults=response_model_exclude_defaults,
            # response_model_exclude_none=response_model_exclude_none,
            # include_in_schema=include_in_schema,
            # response_class=response_class,
            name=name,
            # openapi_extra=openapi_extra,
            # generate_unique_id_function=generate_unique_id_function,
        )
        return self

    def add_static_route(
        self, route_path: str, directory: Path, name: str = "static"
    ) -> "Configurator":
        """
        Mount a directory to an http endpoint.

        :param route_path: the root path for the statics
        :param directory: the directory on the filesystem where the statics files are.
        :param name: a name for the route in the starlette app.
        :return: the configurator

        """
        self._app.mount(route_path, StaticFiles(directory=directory), name=name)
        return self

    def add_exception_handler(
        self, status_code_or_exc: int | Type[Exception], handler: Any
    ) -> "Configurator":
        """Add an exception handler the application."""

        def exception_handler(request: Request, exc: Exception) -> Any:
            req = FastlifeRequest(self.registry, request)
            return handler(req, exc)

        self._app.add_exception_handler(status_code_or_exc, exception_handler)
        return self


def configure(
    wrapped: Callable[[Configurator], None]
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

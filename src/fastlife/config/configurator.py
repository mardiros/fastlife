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

import logging
from asyncio import iscoroutine
from collections import defaultdict
from collections.abc import Callable, Sequence
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Annotated, Any, Generic, Self, TypeVar

import venusian
from fastapi import Depends, FastAPI, Response
from fastapi import Request as BaseRequest
from fastapi.params import Depends as DependsType
from fastapi.staticfiles import StaticFiles
from fastapi.types import IncEx

from fastlife.adapters.fastapi.request import GenericRequest, Request
from fastlife.adapters.fastapi.routing.route import Route
from fastlife.adapters.fastapi.routing.router import Router
from fastlife.config.openapiextra import OpenApiTag
from fastlife.domain.model.template import InlineTemplate
from fastlife.middlewares.base import AbstractMiddleware
from fastlife.service.check_permission import check_permission
from fastlife.service.csrf import check_csrf
from fastlife.service.registry import DefaultRegistry, TRegistry
from fastlife.settings import Settings
from fastlife.shared_utils.infer import is_inline_template_returned
from fastlife.shared_utils.resolver import (
    resolve,
    resolve_maybe_relative,
)

if TYPE_CHECKING:
    from fastlife.service.locale_negociator import LocaleNegociator  # coverage: ignore
    from fastlife.service.request_factory import (
        RequestFactoryBuilder,  # coverage: ignore
    )
    from fastlife.service.security_policy import AbstractSecurityPolicy
    from fastlife.service.templates import (
        AbstractTemplateRendererFactory,  # coverage: ignore
    )

log = logging.getLogger(__name__)
VENUSIAN_CATEGORY = "fastlife"

venusian_ignored_item = str | Callable[[str], bool]


class ConfigurationError(Exception):
    """
    Error raised during configuration, to avoid errors at runtime.
    """


def rebuild_router(router: Router) -> Router:
    """
    Fix the router.

    FastAPI routers has dependencies that are injected to routes where they are added.

    It means that if you add a dependencies in the router after the route has
    been added, then the dependencies is missing in the route added before.

    To prenvents issues, we rebuild the router route with the dependency.

    :param router: the router to rebuild
    :return: a new router with fixed routes.
    """
    if not router.dependencies:
        return router
    _router = Router(prefix=router.prefix)
    _router.dependencies = router.dependencies
    route: Route
    for route in router.routes:  # type: ignore
        dependencies = [
            dep for dep in route.dependencies if dep not in _router.dependencies
        ]
        _router.add_api_route(
            path=route.path,
            endpoint=route.endpoint,
            response_model=route.response_model,
            status_code=route.status_code,
            tags=route.tags,
            dependencies=dependencies,
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
    return _router


class GenericConfigurator(Generic[TRegistry]):
    """
    Configure and build an application.

    Initialize the app from the settings.
    """

    registry: TRegistry

    def __init__(self, settings: Settings) -> None:
        """
        :param settings: application settings.
        """
        registry_cls = resolve(settings.registry_class)
        self.registry = registry_cls(settings)
        Route._registry = self.registry  # type: ignore

        self.middlewares: list[tuple[type[AbstractMiddleware], Any]] = []
        self.exception_handlers: list[tuple[int | type[Exception], Any]] = []
        self.mounts: list[tuple[str, Path, str]] = []
        self.tags: dict[str, OpenApiTag] = {}

        self.api_title = "OpenAPI"
        self.api_version = "v1"
        self.api_description: str = ""
        self.api_summary: str | None = None
        self.api_swagger_ui_url: str | None = None
        self.api_redoc_url: str | None = None

        self._route_prefix: str = ""
        self._routers: dict[str, Router] = defaultdict(Router)
        self._security_policies: dict[
            str, type[AbstractSecurityPolicy[Any, Any, TRegistry]]
        ] = {}

        self._registered_permissions: set[str] = set()

        self._renderer_globals: dict[str, Any] = {}
        self.scanner = venusian.Scanner(fastlife=self)
        self.include("fastlife.views")
        self.include("fastlife.middlewares")

    @property
    def _current_router(self) -> Router:
        return self._routers[self._route_prefix]

    @property
    def all_registered_permissions(self) -> Sequence[str]:
        """
        Get the list of registered permissions.

        This is usefull for introspection or testing purpose.
        """
        return sorted(self._registered_permissions)

    def build_asgi_app(self) -> FastAPI:
        """
        Build the app after configuration in order to start after beeing configured.

        :return: FastAPI application.
        """

        # register our main template renderer at then end, to ensure that
        # if settings have been manipulated, everythins is taken into account.
        self.add_renderer(
            self.registry.settings.jinjax_file_ext,
            resolve("fastlife.adapters.jinjax.renderer:JinjaxEngine")(
                self.registry.settings
            ),
        )

        app = FastAPI(
            title=self.api_title,
            version=self.api_version,
            description=self.api_description,
            summary=self.api_summary,
            dependencies=[Depends(check_csrf())],
            docs_url=self.api_swagger_ui_url,
            redoc_url=self.api_redoc_url,
            lifespan=self.registry.lifespan,
            openapi_tags=[tag.model_dump(by_alias=True) for tag in self.tags.values()]
            if self.tags
            else None,
        )
        app.router.route_class = Route

        for middleware_class, options in self.middlewares:
            app.add_middleware(middleware_class, **options)  # type: ignore

        for status_code_or_exc, exception_handler in self.exception_handlers:
            app.add_exception_handler(status_code_or_exc, exception_handler)

        for prefix, router in self._routers.items():
            app.include_router(rebuild_router(router), prefix=prefix)

        for route_path, directory, name in self.mounts:
            app.mount(route_path, StaticFiles(directory=directory), name=name)
        return app

    def include(
        self,
        module: str | ModuleType,
        route_prefix: str = "",
        ignore: venusian_ignored_item | Sequence[venusian_ignored_item] | None = None,
    ) -> Self:
        """
        Include a module in order to load its configuration.

        It will scan and load all the submodule until you add an ignore rule.

        The `ignore` argument allows you to ignore certain modules.
        If it is a scrint, it can be an absolute module name or a relative
        one, if starts with a dot.

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
        :param route_prefix: prepend all included route with a prefix
        :param ignore: ignore submodules
        """
        if isinstance(module, str):
            try:
                module = resolve_maybe_relative(module, stack_depth=2)
            except ModuleNotFoundError as exc:
                raise ConfigurationError(f"Can't resolve {module}") from exc

        old, self._route_prefix = self._route_prefix, route_prefix
        try:
            self.scanner.scan(  # type: ignore
                module,
                categories=[VENUSIAN_CATEGORY],
                ignore=ignore,
            )
        finally:
            self._route_prefix = old
        return self

    def set_request_factory(
        self, request_factory: "RequestFactoryBuilder[TRegistry]"
    ) -> Self:
        """Install a request factory, to use a custom request classes."""
        self.registry.request_factory = request_factory(self.registry)
        return self

    def set_locale_negociator(self, locale_negociator: "LocaleNegociator") -> Self:
        """Install a locale negociator for the app."""
        self.registry.locale_negociator = locale_negociator
        return self

    def add_translation_dirs(self, locales_dir: str) -> Self:
        """
        Add a translation directory for localization.

        Usually, the locales is a directory from a package and has to be
        passed with a `:` separator: {package_name}:locales.

        :param locales_dir: the directory contains local inside a python package.
        """
        self.registry.localizer.load(locales_dir)
        return self

    def set_api_documentation_info(
        self,
        title: str,
        version: str,
        description: str,
        *,
        summary: str | None = None,
        swagger_ui_url: str | None = None,
        redoc_url: str | None = None,
    ) -> Self:
        """
        Set your api documentation title for application that expose an API.

        :param title: OpenAPI documentation title
        :param version: OpenAPI api version
        :param description: OpenAPI documentation description. Use markdown here.
        :param summary: OpenAPI documentation summary.
            A short description: text only.
        :param swagger_ui_url: Endpoint for {term}`Swagger UI` served by FastAPI
        :param redoc_url: Endpoint for {term}`Redoc` served by FastAPI
        """
        self.api_title = title
        self.api_version = version
        self.api_description = description
        self.api_summary = summary
        self.api_swagger_ui_url = swagger_ui_url
        self.api_redoc_url = redoc_url
        return self

    def add_openapi_tag(self, tag: OpenApiTag) -> Self:
        """Register a tag description in the {term}`OpenAPI` documentation."""
        if tag.name in self.tags:
            raise ConfigurationError(f"Tag {tag.name} can't be registered twice.")
        self.tags[tag.name] = tag
        return self

    def add_middleware(
        self, middleware_class: type[AbstractMiddleware], **options: Any
    ) -> Self:
        """
        Add a starlette middleware to the FastAPI app.
        """
        self.middlewares.append((middleware_class, options))
        return self

    def set_security_policy(
        self, security_policy: "type[AbstractSecurityPolicy[TRegistry, Any, Any]]"
    ) -> Self:
        """
        Set a security policy for the application.

        ```{important}
        The security policy is **per route_prefix**.
        It means that if the application is splitted via multiple
        route_prefix using the {meth}`Configurator.include`, they
        all have a distinct security policy. A secutity policy has
        to be install by all of those include call.

        :param security_policy: The security policy that will applied for the app
            portion behind the route prefix.
        ```
        """
        self._security_policies[self._route_prefix] = security_policy
        self._current_router.dependencies.append(Depends(security_policy))
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
        {func}`fastlife.config.configurator.configure` has to be used to
        inject routes inside a method and call the add_route method.

        This route has to be used to add API Route, by API, to expose it in the
        documentation.

        To add a route that serve HTML user the method {meth}`Configurator.add_route`

        :param name: name of the route, used to build route from the helper
            {meth}`fastlife.request.request.Request.url_for` in order to create links.
        :param path: path of the route, use `{curly_brace}` to inject FastAPI Path
            parameters.
        :param endpoint: the function that will reveive the request.
        :param permission: a permission to validate by the security policy.
        :param methods: restrict route to a list of http methods.
        :param description:{term}`OpenAPI` description for the route.
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
        :param openapi_extra: OpenAPI documentation extra fields.

        :return: the configurator.
        """
        dependencies: list[DependsType] = []
        if permission:
            self._registered_permissions.add(permission)
            dependencies.append(Depends(check_permission(permission)))

        self._current_router.add_api_route(
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

    def add_renderer_global(
        self, name: str, value: Any, *, evaluate: bool = True
    ) -> None:
        """
        Add a rendering global value.

        :param name: the name or key of the global value available in the template.
        :param value: a value, or a callable or
            an async function with a request in parameter that will evaluate the value.
        :param evaluate: set to false if you want to inject helper methods in the
            template.
        """
        self._renderer_globals[name] = value, evaluate

    async def _build_renderer_globals(self, request: Request) -> dict[str, Any]:
        """
        Build globals variables accessible in any templates.

        * `request` is the {class}`current request <fastlife.request.request.Request>`
        * `authenticated_user` is used to access to the authenticated user if the
            security policy has been installed.
        * `csrf_token` is used to build for {jinjax:component}`CsrfToken`.
        * `gettext`, `ngettext`, `dgettext`, `dngettext`, `pgettext`, `dpgettext`,
        `npgettext`, `dnpgettext` methods are installed for i18n purpose.
        """
        lczr = request.registry.localizer(request.locale_name)
        custom_globals = {}
        for key, (val, evaluate) in self._renderer_globals.items():
            if evaluate and callable(val):
                val = val(request)
                if iscoroutine(val):
                    val = await val
            custom_globals[key] = val
        return {
            "request": request,
            "gettext": lczr.gettext,
            "ngettext": lczr.ngettext,
            "dgettext": lczr.dgettext,
            "dngettext": lczr.dngettext,
            "pgettext": lczr.pgettext,
            "dpgettext": lczr.dpgettext,
            "npgettext": lczr.npgettext,
            "dnpgettext": lczr.dnpgettext,
            **custom_globals,
            **request.renderer_globals,
        }

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
            {meth}`fastlife.request.request.Request.url_for` in order to create links.
        :param path: path of the route, use `{curly_brace}` to inject FastAPI Path
            parameters.
        :param endpoint: the function that will reveive the request.
        :param permission: a permission to validate by the
            {class}`Security Policy <fastlife.service.security_policy.AbstractSecurityPolicy>`.
        :param status_code: customize response status code.
        :param methods: restrict route to a list of http methods.
        :return: the configurator.
        """
        dependencies: list[DependsType] = []
        if permission:
            self._registered_permissions.add(permission)
            dependencies.append(Depends(check_permission(permission)))

        if is_inline_template_returned(endpoint):

            async def render(
                request: Request,
                resp: Annotated["Response | InlineTemplate", Depends(endpoint)],
            ) -> Response:
                if isinstance(resp, Response):
                    return resp

                template = resp.renderer
                globs = await self._build_renderer_globals(request)
                return request.registry.get_renderer(template)(request).render(
                    template,
                    params=resp,
                    globals=globs,
                )

            endpoint = render

        self._current_router.add_api_route(
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
        self,
        status_code_or_exc: int | type[Exception],
        handler: Callable[..., "Response | InlineTemplate"],
        *,
        status_code: int = 500,
    ) -> Self:
        """
        Add an exception handler the application.

        """

        async def exception_handler(request: BaseRequest, exc: Exception) -> Any:
            # FastAPI exception handler does not provide our request object
            # it seems like it is rebuild from the asgi scope. Even the router
            # class is wrong.
            # Until we store a security policy per rooter, we rebuild an
            # incomplete request here.
            req = GenericRequest[DefaultRegistry, Any, Any](self.registry, request)
            resp = handler(req, exc)
            if isinstance(resp, Response):
                return resp

            return req.registry.get_renderer(resp.renderer)(req).render(
                resp.template,
                params=resp,
                status_code=status_code,
                globals=(await self._build_renderer_globals(req)),
            )

        self.exception_handlers.append((status_code_or_exc, exception_handler))
        return self

    def add_renderer(
        self, file_ext: str, renderer: "AbstractTemplateRendererFactory"
    ) -> Self:
        """
        Add a render for a given file extension.

        :param file_ext: the file extention of your templates.
        :param renderer: the renderer that will render the template.
        """
        # we don't want to expose the renderer publicly as mutable
        self.registry.renderers[f".{file_ext.lstrip('.')}"] = renderer  # type: ignore
        return self

    def add_template_search_path(self, path: str | Path) -> Self:
        """
        Add a template search path directly from the code.

        :param path: template path.
        """
        self.registry.settings.template_search_path = (
            f"{self.registry.settings.template_search_path},{path}"
        )
        return self


class Configurator(GenericConfigurator[DefaultRegistry]):
    """
    Configure and build an application.

    Initialize the app from the settings.
    """


TConfigurator = TypeVar("TConfigurator", bound=GenericConfigurator[Any])


def configure(
    wrapped: Callable[[TConfigurator], None],
) -> Callable[[Any], None]:
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

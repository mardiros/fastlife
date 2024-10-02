# {py:mod}`fastlife.config.configurator`

```{py:module} fastlife.config.configurator
```

```{autodoc2-docstring} fastlife.config.configurator
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Configurator <fastlife.config.configurator.Configurator>`
  - ```{autodoc2-docstring} fastlife.config.configurator.Configurator
    :parser: myst
    :summary:
    ```
* - {py:obj}`GenericConfigurator <fastlife.config.configurator.GenericConfigurator>`
  - ```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`configure <fastlife.config.configurator.configure>`
  - ```{autodoc2-docstring} fastlife.config.configurator.configure
    :parser: myst
    :summary:
    ```
* - {py:obj}`rebuild_router <fastlife.config.configurator.rebuild_router>`
  - ```{autodoc2-docstring} fastlife.config.configurator.rebuild_router
    :parser: myst
    :summary:
    ```
````

### API

````{py:exception} ConfigurationError()
:canonical: fastlife.config.configurator.ConfigurationError

Bases: {py:obj}`Exception`

```{autodoc2-docstring} fastlife.config.configurator.ConfigurationError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.configurator.ConfigurationError.__init__
:parser: myst
```

````

````{py:class} Configurator(settings: fastlife.config.settings.Settings)
:canonical: fastlife.config.configurator.Configurator

Bases: {py:obj}`fastlife.config.configurator.GenericConfigurator`\[{py:obj}`fastlife.config.registry.DefaultRegistry`\]

```{autodoc2-docstring} fastlife.config.configurator.Configurator
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.configurator.Configurator.__init__
:parser: myst
```

````

`````{py:class} GenericConfigurator(settings: fastlife.config.settings.Settings)
:canonical: fastlife.config.configurator.GenericConfigurator

Bases: {py:obj}`typing.Generic`\[{py:obj}`fastlife.config.registry.TRegistry`\]

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.__init__
:parser: myst
```

````{py:method} add_api_route(name: str, path: str, endpoint: typing.Callable[..., typing.Any], *, permission: str | None = None, status_code: int | None = None, tags: list[str | enum.Enum] | None = None, summary: str | None = None, description: str | None = None, response_description: str = 'Successful Response', deprecated: bool | None = None, methods: list[str] | None = None, operation_id: str | None = None, response_model_include: fastapi.types.IncEx | None = None, response_model_exclude: fastapi.types.IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, include_in_schema: bool = True, openapi_extra: dict[str, typing.Any] | None = None) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_api_route

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_api_route
:parser: myst
```

````

````{py:method} add_exception_handler(status_code_or_exc: int | typing.Type[Exception], handler: typing.Any, *, template: str | None = None, status_code: int = 500) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_exception_handler

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_exception_handler
:parser: myst
```

````

````{py:method} add_middleware(middleware_class: typing.Type[fastlife.middlewares.base.AbstractMiddleware], **options: typing.Any) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_middleware

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_middleware
:parser: myst
```

````

````{py:method} add_open_tag(tag: fastlife.config.openapiextra.OpenApiTag) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_open_tag

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_open_tag
:parser: myst
```

````

````{py:method} add_renderer(file_ext: str, renderer: fastlife.services.templates.AbstractTemplateRendererFactory) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_renderer

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_renderer
:parser: myst
```

````

````{py:method} add_route(name: str, path: str, endpoint: typing.Callable[..., typing.Any], *, permission: str | None = None, template: str | None = None, status_code: int | None = None, methods: list[str] | None = None) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_route

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_route
:parser: myst
```

````

````{py:method} add_static_route(route_path: str, directory: pathlib.Path, name: str = 'static') -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_static_route

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_static_route
:parser: myst
```

````

````{py:method} add_template_search_path(path: str | pathlib.Path) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_template_search_path

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_template_search_path
:parser: myst
```

````

````{py:method} add_translation_dirs(locales_dir: str) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.add_translation_dirs

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.add_translation_dirs
:parser: myst
```

````

````{py:method} build_asgi_app() -> fastapi.FastAPI
:canonical: fastlife.config.configurator.GenericConfigurator.build_asgi_app

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.build_asgi_app
:parser: myst
```

````

````{py:method} include(module: str | types.ModuleType, route_prefix: str = '', ignore: fastlife.config.configurator.venusian_ignored_item | collections.abc.Sequence[fastlife.config.configurator.venusian_ignored_item] | None = None) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.include

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.include
:parser: myst
```

````

````{py:method} set_api_documentation_info(title: str, version: str, description: str, *, summary: str | None = None, swagger_ui_url: str | None = None, redoc_url: str | None = None) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.set_api_documentation_info

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.set_api_documentation_info
:parser: myst
```

````

````{py:method} set_locale_negociator(locale_negociator: fastlife.services.locale_negociator.LocaleNegociator) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.set_locale_negociator

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.set_locale_negociator
:parser: myst
```

````

````{py:method} set_security_policy(security_policy: type[AbstractSecurityPolicy[Any]]) -> typing.Self
:canonical: fastlife.config.configurator.GenericConfigurator.set_security_policy

```{autodoc2-docstring} fastlife.config.configurator.GenericConfigurator.set_security_policy
:parser: myst
```

````

`````

````{py:function} configure(wrapped: typing.Callable[[fastlife.config.configurator.Configurator], None]) -> typing.Callable[[typing.Any], None]
:canonical: fastlife.config.configurator.configure

```{autodoc2-docstring} fastlife.config.configurator.configure
:parser: myst
```
````

````{py:function} rebuild_router(router: fastlife.routing.router.Router) -> fastlife.routing.router.Router
:canonical: fastlife.config.configurator.rebuild_router

```{autodoc2-docstring} fastlife.config.configurator.rebuild_router
:parser: myst
```
````

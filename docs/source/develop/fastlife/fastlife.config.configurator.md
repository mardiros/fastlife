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
* - {py:obj}`ExternalDocs <fastlife.config.configurator.ExternalDocs>`
  -
* - {py:obj}`OpenApiTag <fastlife.config.configurator.OpenApiTag>`
  -
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
````

### API

`````{py:class} Configurator(settings: fastlife.config.settings.Settings)
:canonical: fastlife.config.configurator.Configurator

```{autodoc2-docstring} fastlife.config.configurator.Configurator
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.configurator.Configurator.__init__
:parser: myst
```

````{py:method} add_api_route(name: str, path: str, endpoint: typing.Callable[..., typing.Any], *, permission: str | None = None, status_code: int | None = None, tags: list[str | enum.Enum] | None = None, summary: str | None = None, description: str | None = None, response_description: str = 'Successful Response', deprecated: bool | None = None, methods: list[str] | None = None, operation_id: str | None = None, response_model_include: fastapi.types.IncEx | None = None, response_model_exclude: fastapi.types.IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, include_in_schema: bool = True, openapi_extra: dict[str, typing.Any] | None = None) -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.add_api_route

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_api_route
:parser: myst
```

````

````{py:method} add_exception_handler(status_code_or_exc: int | typing.Type[Exception], handler: typing.Any) -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.add_exception_handler

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_exception_handler
:parser: myst
```

````

````{py:method} add_middleware(middleware_class: typing.Type[fastlife.middlewares.base.AbstractMiddleware], **options: typing.Any) -> typing.Self
:canonical: fastlife.config.configurator.Configurator.add_middleware

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_middleware
:parser: myst
```

````

````{py:method} add_route(name: str, path: str, endpoint: typing.Callable[..., typing.Any], *, permission: str | None = None, status_code: int | None = None, methods: list[str] | None = None) -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.add_route

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_route
:parser: myst
```

````

````{py:method} add_static_route(route_path: str, directory: pathlib.Path, name: str = 'static') -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.add_static_route

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_static_route
:parser: myst
```

````

````{py:method} get_asgi_app() -> fastapi.FastAPI
:canonical: fastlife.config.configurator.Configurator.get_asgi_app

```{autodoc2-docstring} fastlife.config.configurator.Configurator.get_asgi_app
:parser: myst
```

````

````{py:method} include(module: str | types.ModuleType) -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.include

```{autodoc2-docstring} fastlife.config.configurator.Configurator.include
:parser: myst
```

````

`````

```{py:class} ExternalDocs(/, **data: typing.Any)
:canonical: fastlife.config.configurator.ExternalDocs

Bases: {py:obj}`pydantic.BaseModel`

```

```{py:class} OpenApiTag(/, **data: typing.Any)
:canonical: fastlife.config.configurator.OpenApiTag

Bases: {py:obj}`pydantic.BaseModel`

```

````{py:function} configure(wrapped: typing.Callable[[fastlife.config.configurator.Configurator], None]) -> typing.Callable[[fastlife.config.configurator.Configurator], None]
:canonical: fastlife.config.configurator.configure

```{autodoc2-docstring} fastlife.config.configurator.configure
:parser: myst
```
````

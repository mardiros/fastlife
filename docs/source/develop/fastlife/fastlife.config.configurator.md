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
  - ```{autodoc2-docstring} fastlife.config.configurator.ExternalDocs
    :parser: myst
    :summary:
    ```
* - {py:obj}`OpenApiTag <fastlife.config.configurator.OpenApiTag>`
  - ```{autodoc2-docstring} fastlife.config.configurator.OpenApiTag
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

````{py:method} add_api_route(name: str, path: str, endpoint: typing.Callable[..., typing.Any], *, permission: str | None = None, status_code: int | None = None, tags: list[str | enum.Enum] | None = None, summary: str | None = None, description: str | None = None, response_description: str = 'Successful Response', deprecated: bool | None = None, methods: list[str] | None = None, operation_id: str | None = None, response_model_include: fastapi.types.IncEx | None = None, response_model_exclude: fastapi.types.IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, include_in_schema: bool = True, openapi_extra: dict[str, typing.Any] | None = None) -> typing.Self
:canonical: fastlife.config.configurator.Configurator.add_api_route

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_api_route
:parser: myst
```

````

````{py:method} add_exception_handler(status_code_or_exc: int | typing.Type[Exception], handler: typing.Any) -> typing.Self
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

````{py:method} add_open_tag(tag: fastlife.config.configurator.OpenApiTag) -> typing.Self
:canonical: fastlife.config.configurator.Configurator.add_open_tag

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_open_tag
:parser: myst
```

````

````{py:method} add_route(name: str, path: str, endpoint: typing.Callable[..., typing.Any], *, permission: str | None = None, template: str | None = None, status_code: int | None = None, methods: list[str] | None = None) -> typing.Self
:canonical: fastlife.config.configurator.Configurator.add_route

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_route
:parser: myst
```

````

````{py:method} add_static_route(route_path: str, directory: pathlib.Path, name: str = 'static') -> typing.Self
:canonical: fastlife.config.configurator.Configurator.add_static_route

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_static_route
:parser: myst
```

````

````{py:method} build_asgi_app() -> fastapi.FastAPI
:canonical: fastlife.config.configurator.Configurator.build_asgi_app

```{autodoc2-docstring} fastlife.config.configurator.Configurator.build_asgi_app
:parser: myst
```

````

````{py:method} include(module: str | types.ModuleType) -> typing.Self
:canonical: fastlife.config.configurator.Configurator.include

```{autodoc2-docstring} fastlife.config.configurator.Configurator.include
:parser: myst
```

````

````{py:method} set_api_documentation_info(title: str, version: str, description: str, summary: str | None = None) -> typing.Self
:canonical: fastlife.config.configurator.Configurator.set_api_documentation_info

```{autodoc2-docstring} fastlife.config.configurator.Configurator.set_api_documentation_info
:parser: myst
```

````

`````

`````{py:class} ExternalDocs(/, **data: typing.Any)
:canonical: fastlife.config.configurator.ExternalDocs

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} fastlife.config.configurator.ExternalDocs
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.configurator.ExternalDocs.__init__
:parser: myst
```

````{py:attribute} description
:canonical: fastlife.config.configurator.ExternalDocs.description
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.config.configurator.ExternalDocs.description
:parser: myst
```

````

````{py:attribute} url
:canonical: fastlife.config.configurator.ExternalDocs.url
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.config.configurator.ExternalDocs.url
:parser: myst
```

````

`````

`````{py:class} OpenApiTag(/, **data: typing.Any)
:canonical: fastlife.config.configurator.OpenApiTag

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} fastlife.config.configurator.OpenApiTag
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.configurator.OpenApiTag.__init__
:parser: myst
```

````{py:attribute} description
:canonical: fastlife.config.configurator.OpenApiTag.description
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.config.configurator.OpenApiTag.description
:parser: myst
```

````

````{py:attribute} external_docs
:canonical: fastlife.config.configurator.OpenApiTag.external_docs
:type: fastlife.config.configurator.ExternalDocs | None
:value: >
   'Field(...)'

```{autodoc2-docstring} fastlife.config.configurator.OpenApiTag.external_docs
:parser: myst
```

````

````{py:attribute} name
:canonical: fastlife.config.configurator.OpenApiTag.name
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.config.configurator.OpenApiTag.name
:parser: myst
```

````

`````

````{py:function} configure(wrapped: typing.Callable[[fastlife.config.configurator.Configurator], None]) -> typing.Callable[[fastlife.config.configurator.Configurator], None]
:canonical: fastlife.config.configurator.configure

```{autodoc2-docstring} fastlife.config.configurator.configure
:parser: myst
```
````

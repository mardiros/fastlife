# {py:mod}`fastlife.config.configurator`

```{py:module} fastlife.config.configurator
```

```{autodoc2-docstring} fastlife.config.configurator
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Configurator <fastlife.config.configurator.Configurator>`
  - ```{autodoc2-docstring} fastlife.config.configurator.Configurator
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`configure <fastlife.config.configurator.configure>`
  - ```{autodoc2-docstring} fastlife.config.configurator.configure
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`log <fastlife.config.configurator.log>`
  - ```{autodoc2-docstring} fastlife.config.configurator.log
    :summary:
    ```
* - {py:obj}`VENUSIAN_CATEGORY <fastlife.config.configurator.VENUSIAN_CATEGORY>`
  - ```{autodoc2-docstring} fastlife.config.configurator.VENUSIAN_CATEGORY
    :summary:
    ```
````

### API

````{py:data} log
:canonical: fastlife.config.configurator.log
:value: >
   'getLogger(...)'

```{autodoc2-docstring} fastlife.config.configurator.log
```

````

````{py:data} VENUSIAN_CATEGORY
:canonical: fastlife.config.configurator.VENUSIAN_CATEGORY
:value: >
   'fastlife'

```{autodoc2-docstring} fastlife.config.configurator.VENUSIAN_CATEGORY
```

````

`````{py:class} Configurator(settings: fastlife.config.settings.Settings)
:canonical: fastlife.config.configurator.Configurator

```{autodoc2-docstring} fastlife.config.configurator.Configurator
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.configurator.Configurator.__init__
```

````{py:attribute} registry
:canonical: fastlife.config.configurator.Configurator.registry
:type: fastlife.config.registry.AppRegistry
:value: >
   None

```{autodoc2-docstring} fastlife.config.configurator.Configurator.registry
```

````

````{py:method} get_asgi_app() -> fastapi.FastAPI
:canonical: fastlife.config.configurator.Configurator.get_asgi_app

```{autodoc2-docstring} fastlife.config.configurator.Configurator.get_asgi_app
```

````

````{py:method} include(module: str | types.ModuleType) -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.include

```{autodoc2-docstring} fastlife.config.configurator.Configurator.include
```

````

````{py:method} add_middleware(middleware_class: typing.Type[fastlife.middlewares.base.AbstractMiddleware], **options: typing.Any) -> typing.Self
:canonical: fastlife.config.configurator.Configurator.add_middleware

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_middleware
```

````

````{py:method} add_route(name: str, path: str, endpoint: typing.Callable[..., typing.Any], *, permission: str | None = None, status_code: int | None = None, tags: typing.List[typing.Union[str, enum.Enum]] | None = None, summary: typing.Optional[str] = None, description: typing.Optional[str] = None, response_description: str = 'Successful Response', deprecated: typing.Optional[bool] = None, methods: typing.Optional[typing.List[str]] = None) -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.add_route

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_route
```

````

````{py:method} add_static_route(route_path: str, directory: pathlib.Path, name: str = 'static') -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.add_static_route

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_static_route
```

````

````{py:method} add_exception_handler(status_code_or_exc: int | typing.Type[Exception], handler: typing.Any) -> fastlife.config.configurator.Configurator
:canonical: fastlife.config.configurator.Configurator.add_exception_handler

```{autodoc2-docstring} fastlife.config.configurator.Configurator.add_exception_handler
```

````

`````

````{py:function} configure(wrapped: typing.Callable[[fastlife.config.configurator.Configurator], None]) -> typing.Callable[[fastlife.config.configurator.Configurator], None]
:canonical: fastlife.config.configurator.configure

```{autodoc2-docstring} fastlife.config.configurator.configure
```
````

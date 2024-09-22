# {py:mod}`fastlife.routing.route`

```{py:module} fastlife.routing.route
```

```{autodoc2-docstring} fastlife.routing.route
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Route <fastlife.routing.route.Route>`
  - ```{autodoc2-docstring} fastlife.routing.route.Route
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} Route(path: str, endpoint: typing.Callable[..., typing.Any], *, response_model: typing.Any = Default(None), status_code: typing.Optional[int] = None, tags: typing.Optional[typing.List[typing.Union[str, enum.Enum]]] = None, dependencies: typing.Optional[typing.Sequence[fastapi.params.Depends]] = None, summary: typing.Optional[str] = None, description: typing.Optional[str] = None, response_description: str = 'Successful Response', responses: typing.Optional[typing.Dict[typing.Union[int, str], typing.Dict[str, typing.Any]]] = None, deprecated: typing.Optional[bool] = None, name: typing.Optional[str] = None, methods: typing.Optional[typing.Union[typing.Set[str], typing.List[str]]] = None, operation_id: typing.Optional[str] = None, response_model_include: typing.Optional[fastapi.types.IncEx] = None, response_model_exclude: typing.Optional[fastapi.types.IncEx] = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, include_in_schema: bool = True, response_class: typing.Union[typing.Type[starlette.responses.Response], fastapi.datastructures.DefaultPlaceholder] = Default(JSONResponse), dependency_overrides_provider: typing.Optional[typing.Any] = None, callbacks: typing.Optional[typing.List[starlette.routing.BaseRoute]] = None, openapi_extra: typing.Optional[typing.Dict[str, typing.Any]] = None, generate_unique_id_function: typing.Union[typing.Callable[[fastapi.routing.APIRoute], str], fastapi.datastructures.DefaultPlaceholder] = Default(generate_unique_id))
:canonical: fastlife.routing.route.Route

Bases: {py:obj}`fastapi.routing.APIRoute`

```{autodoc2-docstring} fastlife.routing.route.Route
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.routing.route.Route.__init__
:parser: myst
```

````{py:method} get_route_handler() -> typing.Callable[[starlette.requests.Request], typing.Coroutine[typing.Any, typing.Any, starlette.responses.Response]]
:canonical: fastlife.routing.route.Route.get_route_handler

```{autodoc2-docstring} fastlife.routing.route.Route.get_route_handler
:parser: myst
```

````

`````

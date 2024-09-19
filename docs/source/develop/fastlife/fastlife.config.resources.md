# {py:mod}`fastlife.config.resources`

```{py:module} fastlife.config.resources
```

```{autodoc2-docstring} fastlife.config.resources
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`resource_view <fastlife.config.resources.resource_view>`
  - ```{autodoc2-docstring} fastlife.config.resources.resource_view
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`resource <fastlife.config.resources.resource>`
  - ```{autodoc2-docstring} fastlife.config.resources.resource
    :parser: myst
    :summary:
    ```
````

### API

````{py:function} resource(name: str, *, path: str | None = None, collection_path: str | None = None, description: str | None = None, external_docs: fastlife.config.configurator.ExternalDocs | None = None) -> typing.Callable[..., typing.Any]
:canonical: fastlife.config.resources.resource

```{autodoc2-docstring} fastlife.config.resources.resource
:parser: myst
```
````

````{py:class} resource_view(permission: str | None = None, status_code: int | None = None, summary: str | None = None, description: str | None = None, response_description: str = 'Successful Response', deprecated: bool | None = None, methods: list[str] | None = None, operation_id: str | None = None, response_model_include: fastapi.types.IncEx | None = None, response_model_exclude: fastapi.types.IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, include_in_schema: bool = True, openapi_extra: dict[str, typing.Any] | None = None)
:canonical: fastlife.config.resources.resource_view

```{autodoc2-docstring} fastlife.config.resources.resource_view
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.config.resources.resource_view.__init__
:parser: myst
```

````

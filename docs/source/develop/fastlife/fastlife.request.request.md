# {py:mod}`fastlife.request.request`

```{py:module} fastlife.request.request
```

```{autodoc2-docstring} fastlife.request.request
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Request <fastlife.request.request.Request>`
  - ```{autodoc2-docstring} fastlife.request.request.Request
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} Request(registry: fastlife.config.registry.AppRegistry, request: fastapi.Request)
:canonical: fastlife.request.request.Request

Bases: {py:obj}`fastapi.Request`

```{autodoc2-docstring} fastlife.request.request.Request
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.request.request.Request.__init__
:parser: myst
```

````{py:method} has_permission(permission: str) -> HasPermission | type[HasPermission]
:canonical: fastlife.request.request.Request.has_permission
:async:

```{autodoc2-docstring} fastlife.request.request.Request.has_permission
:parser: myst
```

````

````{py:attribute} locale_name
:canonical: fastlife.request.request.Request.locale_name
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.Request.locale_name
:parser: myst
```

````

````{py:attribute} registry
:canonical: fastlife.request.request.Request.registry
:type: fastlife.config.registry.AppRegistry
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.Request.registry
:parser: myst
```

````

````{py:attribute} security_policy
:canonical: fastlife.request.request.Request.security_policy
:type: AbstractSecurityPolicy[Any] | None
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.Request.security_policy
:parser: myst
```

````

`````

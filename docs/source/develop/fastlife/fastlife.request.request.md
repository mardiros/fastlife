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

* - {py:obj}`GenericRequest <fastlife.request.request.GenericRequest>`
  - ```{autodoc2-docstring} fastlife.request.request.GenericRequest
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AnyRequest <fastlife.request.request.AnyRequest>`
  - ```{autodoc2-docstring} fastlife.request.request.AnyRequest
    :parser: myst
    :summary:
    ```
* - {py:obj}`Registry <fastlife.request.request.Registry>`
  - ```{autodoc2-docstring} fastlife.request.request.Registry
    :parser: myst
    :summary:
    ```
* - {py:obj}`Request <fastlife.request.request.Request>`
  - ```{autodoc2-docstring} fastlife.request.request.Request
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} AnyRequest
:canonical: fastlife.request.request.AnyRequest
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.AnyRequest
:parser: myst
```

````

`````{py:class} GenericRequest(registry: fastlife.config.registry.TRegistry, request: fastapi.Request)
:canonical: fastlife.request.request.GenericRequest

Bases: {py:obj}`fastapi.Request`, {py:obj}`typing_extensions.Generic`\[{py:obj}`fastlife.config.registry.TRegistry`\]

```{autodoc2-docstring} fastlife.request.request.GenericRequest
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.request.request.GenericRequest.__init__
:parser: myst
```

````{py:method} has_permission(permission: str) -> HasPermission | type[HasPermission]
:canonical: fastlife.request.request.GenericRequest.has_permission
:async:

```{autodoc2-docstring} fastlife.request.request.GenericRequest.has_permission
:parser: myst
```

````

````{py:attribute} locale_name
:canonical: fastlife.request.request.GenericRequest.locale_name
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.GenericRequest.locale_name
:parser: myst
```

````

````{py:attribute} registry
:canonical: fastlife.request.request.GenericRequest.registry
:type: fastlife.config.registry.TRegistry
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.GenericRequest.registry
:parser: myst
```

````

````{py:attribute} security_policy
:canonical: fastlife.request.request.GenericRequest.security_policy
:type: AbstractSecurityPolicy[Any] | None
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.GenericRequest.security_policy
:parser: myst
```

````

`````

````{py:data} Registry
:canonical: fastlife.request.request.Registry
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.Registry
:parser: myst
```

````

````{py:data} Request
:canonical: fastlife.request.request.Request
:value: >
   None

```{autodoc2-docstring} fastlife.request.request.Request
:parser: myst
```

````

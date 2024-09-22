# {py:mod}`fastlife.middlewares.base`

```{py:module} fastlife.middlewares.base
```

```{autodoc2-docstring} fastlife.middlewares.base
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AbstractMiddleware <fastlife.middlewares.base.AbstractMiddleware>`
  - ```{autodoc2-docstring} fastlife.middlewares.base.AbstractMiddleware
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} AbstractMiddleware
:canonical: fastlife.middlewares.base.AbstractMiddleware

Bases: {py:obj}`abc.ABC`

```{autodoc2-docstring} fastlife.middlewares.base.AbstractMiddleware
:parser: myst
```

````{py:method} __call__(scope: starlette.types.Scope, receive: starlette.types.Receive, send: starlette.types.Send) -> None
:canonical: fastlife.middlewares.base.AbstractMiddleware.__call__
:abstractmethod:
:async:

```{autodoc2-docstring} fastlife.middlewares.base.AbstractMiddleware.__call__
:parser: myst
```

````

`````

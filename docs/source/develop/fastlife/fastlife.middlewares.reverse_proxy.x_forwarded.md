---
orphan: true
---

# {py:mod}`fastlife.middlewares.reverse_proxy.x_forwarded`

```{py:module} fastlife.middlewares.reverse_proxy.x_forwarded
```

```{autodoc2-docstring} fastlife.middlewares.reverse_proxy.x_forwarded
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`XForwardedStar <fastlife.middlewares.reverse_proxy.x_forwarded.XForwardedStar>`
  -
````

### API

`````{py:class} XForwardedStar(app: starlette.types.ASGIApp)
:canonical: fastlife.middlewares.reverse_proxy.x_forwarded.XForwardedStar

Bases: {py:obj}`fastlife.middlewares.base.AbstractMiddleware`

````{py:method} __call__(scope: starlette.types.Scope, receive: starlette.types.Receive, send: starlette.types.Send) -> None
:canonical: fastlife.middlewares.reverse_proxy.x_forwarded.XForwardedStar.__call__
:async:

````

`````

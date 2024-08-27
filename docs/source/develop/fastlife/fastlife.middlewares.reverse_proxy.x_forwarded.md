# {py:mod}`fastlife.middlewares.reverse_proxy.x_forwarded`

```{py:module} fastlife.middlewares.reverse_proxy.x_forwarded
```

```{autodoc2-docstring} fastlife.middlewares.reverse_proxy.x_forwarded
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

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_header <fastlife.middlewares.reverse_proxy.x_forwarded.get_header>`
  - ```{autodoc2-docstring} fastlife.middlewares.reverse_proxy.x_forwarded.get_header
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`log <fastlife.middlewares.reverse_proxy.x_forwarded.log>`
  - ```{autodoc2-docstring} fastlife.middlewares.reverse_proxy.x_forwarded.log
    :summary:
    ```
````

### API

````{py:data} log
:canonical: fastlife.middlewares.reverse_proxy.x_forwarded.log
:value: >
   'getLogger(...)'

```{autodoc2-docstring} fastlife.middlewares.reverse_proxy.x_forwarded.log
```

````

````{py:function} get_header(headers: typing.Sequence[typing.Tuple[bytes, bytes]], key: bytes) -> typing.Optional[str]
:canonical: fastlife.middlewares.reverse_proxy.x_forwarded.get_header

```{autodoc2-docstring} fastlife.middlewares.reverse_proxy.x_forwarded.get_header
```
````

`````{py:class} XForwardedStar(app: starlette.types.ASGIApp)
:canonical: fastlife.middlewares.reverse_proxy.x_forwarded.XForwardedStar

Bases: {py:obj}`fastlife.middlewares.base.AbstractMiddleware`

````{py:method} __call__(scope: starlette.types.Scope, receive: starlette.types.Receive, send: starlette.types.Send) -> None
:canonical: fastlife.middlewares.reverse_proxy.x_forwarded.XForwardedStar.__call__
:async:

````

`````

# {py:mod}`fastlife.middlewares.session.middleware`

```{py:module} fastlife.middlewares.session.middleware
```

```{autodoc2-docstring} fastlife.middlewares.session.middleware
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SessionMiddleware <fastlife.middlewares.session.middleware.SessionMiddleware>`
  - ```{autodoc2-docstring} fastlife.middlewares.session.middleware.SessionMiddleware
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} SessionMiddleware(app: starlette.types.ASGIApp, cookie_name: str, secret_key: str, duration: datetime.timedelta, cookie_path: str = '/', cookie_same_site: typing.Literal[lax, strict, none] = 'lax', cookie_secure: bool = False, cookie_domain: str = '', serializer: typing.Type[fastlife.middlewares.session.serializer.AbsractSessionSerializer] = SignedSessionSerializer)
:canonical: fastlife.middlewares.session.middleware.SessionMiddleware

Bases: {py:obj}`fastlife.middlewares.base.AbstractMiddleware`

```{autodoc2-docstring} fastlife.middlewares.session.middleware.SessionMiddleware
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.middlewares.session.middleware.SessionMiddleware.__init__
:parser: myst
```

````{py:method} __call__(scope: starlette.types.Scope, receive: starlette.types.Receive, send: starlette.types.Send) -> None
:canonical: fastlife.middlewares.session.middleware.SessionMiddleware.__call__
:async:

```{autodoc2-docstring} fastlife.middlewares.session.middleware.SessionMiddleware.__call__
:parser: myst
```

````

`````

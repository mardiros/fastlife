# {py:mod}`fastlife.security.csrf`

```{py:module} fastlife.security.csrf
```

```{autodoc2-docstring} fastlife.security.csrf
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`check_csrf <fastlife.security.csrf.check_csrf>`
  - ```{autodoc2-docstring} fastlife.security.csrf.check_csrf
    :parser: myst
    :summary:
    ```
* - {py:obj}`create_csrf_token <fastlife.security.csrf.create_csrf_token>`
  - ```{autodoc2-docstring} fastlife.security.csrf.create_csrf_token
    :parser: myst
    :summary:
    ```
````

### API

````{py:exception} CSRFAttack()
:canonical: fastlife.security.csrf.CSRFAttack

Bases: {py:obj}`Exception`

```{autodoc2-docstring} fastlife.security.csrf.CSRFAttack
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.csrf.CSRFAttack.__init__
:parser: myst
```

````

````{py:function} check_csrf() -> typing.Callable[[fastlife.request.Request], typing.Coroutine[typing.Any, typing.Any, bool]]
:canonical: fastlife.security.csrf.check_csrf

```{autodoc2-docstring} fastlife.security.csrf.check_csrf
:parser: myst
```
````

````{py:function} create_csrf_token() -> str
:canonical: fastlife.security.csrf.create_csrf_token

```{autodoc2-docstring} fastlife.security.csrf.create_csrf_token
:parser: myst
```
````

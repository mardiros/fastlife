# {py:mod}`fastlife.security.csrf`

```{py:module} fastlife.security.csrf
```

```{autodoc2-docstring} fastlife.security.csrf
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`create_csrf_token <fastlife.security.csrf.create_csrf_token>`
  - ```{autodoc2-docstring} fastlife.security.csrf.create_csrf_token
    :summary:
    ```
* - {py:obj}`check_csrf <fastlife.security.csrf.check_csrf>`
  - ```{autodoc2-docstring} fastlife.security.csrf.check_csrf
    :summary:
    ```
````

### API

````{py:exception} CSRFAttack()
:canonical: fastlife.security.csrf.CSRFAttack

Bases: {py:obj}`Exception`

```{autodoc2-docstring} fastlife.security.csrf.CSRFAttack
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.csrf.CSRFAttack.__init__
```

````

````{py:function} create_csrf_token() -> str
:canonical: fastlife.security.csrf.create_csrf_token

```{autodoc2-docstring} fastlife.security.csrf.create_csrf_token
```
````

````{py:function} check_csrf() -> typing.Callable[[fastlife.request.Request], typing.Coroutine[typing.Any, typing.Any, bool]]
:canonical: fastlife.security.csrf.check_csrf

```{autodoc2-docstring} fastlife.security.csrf.check_csrf
```
````

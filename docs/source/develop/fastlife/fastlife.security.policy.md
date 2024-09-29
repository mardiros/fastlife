# {py:mod}`fastlife.security.policy`

```{py:module} fastlife.security.policy
```

```{autodoc2-docstring} fastlife.security.policy
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AbstractSecurityPolicy <fastlife.security.policy.AbstractSecurityPolicy>`
  - ```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy
    :parser: myst
    :summary:
    ```
* - {py:obj}`Allowed <fastlife.security.policy.Allowed>`
  - ```{autodoc2-docstring} fastlife.security.policy.Allowed
    :parser: myst
    :summary:
    ```
* - {py:obj}`Denied <fastlife.security.policy.Denied>`
  - ```{autodoc2-docstring} fastlife.security.policy.Denied
    :parser: myst
    :summary:
    ```
* - {py:obj}`HasPermission <fastlife.security.policy.HasPermission>`
  -
* - {py:obj}`InsecurePolicy <fastlife.security.policy.InsecurePolicy>`
  - ```{autodoc2-docstring} fastlife.security.policy.InsecurePolicy
    :parser: myst
    :summary:
    ```
* - {py:obj}`Unauthenticated <fastlife.security.policy.Unauthenticated>`
  - ```{autodoc2-docstring} fastlife.security.policy.Unauthenticated
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} AbstractSecurityPolicy(request: fastlife.Request)
:canonical: fastlife.security.policy.AbstractSecurityPolicy

Bases: {py:obj}`abc.ABC`, {py:obj}`typing_extensions.Generic`\[{py:obj}`fastlife.security.policy.TUser`\]

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy.__init__
:parser: myst
```

````{py:attribute} Forbidden
:canonical: fastlife.security.policy.AbstractSecurityPolicy.Forbidden
:value: >
   None

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy.Forbidden
:parser: myst
```

````

````{py:attribute} Unauthorized
:canonical: fastlife.security.policy.AbstractSecurityPolicy.Unauthorized
:value: >
   None

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy.Unauthorized
:parser: myst
```

````

````{py:method} authenticated_userid() -> str | uuid.UUID | None
:canonical: fastlife.security.policy.AbstractSecurityPolicy.authenticated_userid
:abstractmethod:
:async:

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy.authenticated_userid
:parser: myst
```

````

````{py:method} forget() -> None
:canonical: fastlife.security.policy.AbstractSecurityPolicy.forget
:abstractmethod:
:async:

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy.forget
:parser: myst
```

````

````{py:method} has_permission(permission: str) -> fastlife.security.policy.HasPermission | type[fastlife.security.policy.HasPermission]
:canonical: fastlife.security.policy.AbstractSecurityPolicy.has_permission
:abstractmethod:
:async:

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy.has_permission
:parser: myst
```

````

````{py:method} identity() -> fastlife.security.policy.TUser | None
:canonical: fastlife.security.policy.AbstractSecurityPolicy.identity
:abstractmethod:
:async:

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy.identity
:parser: myst
```

````

````{py:method} remember(user: fastlife.security.policy.TUser) -> None
:canonical: fastlife.security.policy.AbstractSecurityPolicy.remember
:abstractmethod:
:async:

```{autodoc2-docstring} fastlife.security.policy.AbstractSecurityPolicy.remember
:parser: myst
```

````

`````

````{py:class} Allowed()
:canonical: fastlife.security.policy.Allowed

Bases: {py:obj}`fastlife.security.policy.HasPermission`

```{autodoc2-docstring} fastlife.security.policy.Allowed
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.policy.Allowed.__init__
:parser: myst
```

````

````{py:class} Denied()
:canonical: fastlife.security.policy.Denied

Bases: {py:obj}`fastlife.security.policy.HasPermission`

```{autodoc2-docstring} fastlife.security.policy.Denied
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.policy.Denied.__init__
:parser: myst
```

````

````{py:exception} Forbidden(status_code: int = HTTP_403_FORBIDDEN, detail: str = 'Forbidden', headers: dict[str, str] | None = None)
:canonical: fastlife.security.policy.Forbidden

Bases: {py:obj}`fastapi.HTTPException`

```{autodoc2-docstring} fastlife.security.policy.Forbidden
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.policy.Forbidden.__init__
:parser: myst
```

````

`````{py:class} HasPermission()
:canonical: fastlife.security.policy.HasPermission

Bases: {py:obj}`int`

````{py:method} __bool__() -> bool
:canonical: fastlife.security.policy.HasPermission.__bool__

````

````{py:method} __new__(reason: str) -> fastlife.security.policy.HasPermission
:canonical: fastlife.security.policy.HasPermission.__new__

````

````{py:method} __repr__() -> str
:canonical: fastlife.security.policy.HasPermission.__repr__

````

`````

`````{py:class} InsecurePolicy(request: fastlife.Request)
:canonical: fastlife.security.policy.InsecurePolicy

Bases: {py:obj}`fastlife.security.policy.AbstractSecurityPolicy`\[{py:obj}`None`\]

```{autodoc2-docstring} fastlife.security.policy.InsecurePolicy
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.policy.InsecurePolicy.__init__
:parser: myst
```

````{py:method} authenticated_userid() -> str | uuid.UUID
:canonical: fastlife.security.policy.InsecurePolicy.authenticated_userid
:async:

```{autodoc2-docstring} fastlife.security.policy.InsecurePolicy.authenticated_userid
:parser: myst
```

````

````{py:method} forget() -> None
:canonical: fastlife.security.policy.InsecurePolicy.forget
:async:

```{autodoc2-docstring} fastlife.security.policy.InsecurePolicy.forget
:parser: myst
```

````

````{py:method} has_permission(permission: str) -> fastlife.security.policy.HasPermission | type[fastlife.security.policy.HasPermission]
:canonical: fastlife.security.policy.InsecurePolicy.has_permission
:async:

```{autodoc2-docstring} fastlife.security.policy.InsecurePolicy.has_permission
:parser: myst
```

````

````{py:method} identity() -> None
:canonical: fastlife.security.policy.InsecurePolicy.identity
:async:

```{autodoc2-docstring} fastlife.security.policy.InsecurePolicy.identity
:parser: myst
```

````

````{py:method} remember(user: None) -> None
:canonical: fastlife.security.policy.InsecurePolicy.remember
:async:

```{autodoc2-docstring} fastlife.security.policy.InsecurePolicy.remember
:parser: myst
```

````

`````

````{py:class} Unauthenticated()
:canonical: fastlife.security.policy.Unauthenticated

Bases: {py:obj}`fastlife.security.policy.HasPermission`

```{autodoc2-docstring} fastlife.security.policy.Unauthenticated
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.policy.Unauthenticated.__init__
:parser: myst
```

````

````{py:exception} Unauthorized(status_code: int = HTTP_401_UNAUTHORIZED, detail: str = 'Unauthorized', headers: dict[str, str] | None = None)
:canonical: fastlife.security.policy.Unauthorized

Bases: {py:obj}`fastapi.HTTPException`

```{autodoc2-docstring} fastlife.security.policy.Unauthorized
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.security.policy.Unauthorized.__init__
:parser: myst
```

````

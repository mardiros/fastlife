# {py:mod}`fastlife.middlewares.session.serializer`

```{py:module} fastlife.middlewares.session.serializer
```

```{autodoc2-docstring} fastlife.middlewares.session.serializer
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AbsractSessionSerializer <fastlife.middlewares.session.serializer.AbsractSessionSerializer>`
  - ```{autodoc2-docstring} fastlife.middlewares.session.serializer.AbsractSessionSerializer
    :parser: myst
    :summary:
    ```
* - {py:obj}`SignedSessionSerializer <fastlife.middlewares.session.serializer.SignedSessionSerializer>`
  - ```{autodoc2-docstring} fastlife.middlewares.session.serializer.SignedSessionSerializer
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} AbsractSessionSerializer(secret_key: str, max_age: int)
:canonical: fastlife.middlewares.session.serializer.AbsractSessionSerializer

Bases: {py:obj}`abc.ABC`

```{autodoc2-docstring} fastlife.middlewares.session.serializer.AbsractSessionSerializer
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.middlewares.session.serializer.AbsractSessionSerializer.__init__
:parser: myst
```

````{py:method} deserialize(data: bytes) -> typing.Tuple[typing.Mapping[str, typing.Any], bool]
:canonical: fastlife.middlewares.session.serializer.AbsractSessionSerializer.deserialize
:abstractmethod:

```{autodoc2-docstring} fastlife.middlewares.session.serializer.AbsractSessionSerializer.deserialize
:parser: myst
```

````

````{py:method} serialize(data: typing.Mapping[str, typing.Any]) -> bytes
:canonical: fastlife.middlewares.session.serializer.AbsractSessionSerializer.serialize
:abstractmethod:

```{autodoc2-docstring} fastlife.middlewares.session.serializer.AbsractSessionSerializer.serialize
:parser: myst
```

````

`````

`````{py:class} SignedSessionSerializer(secret_key: str, max_age: int)
:canonical: fastlife.middlewares.session.serializer.SignedSessionSerializer

Bases: {py:obj}`fastlife.middlewares.session.serializer.AbsractSessionSerializer`

```{autodoc2-docstring} fastlife.middlewares.session.serializer.SignedSessionSerializer
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.middlewares.session.serializer.SignedSessionSerializer.__init__
:parser: myst
```

````{py:method} deserialize(data: bytes) -> typing.Tuple[typing.Mapping[str, typing.Any], bool]
:canonical: fastlife.middlewares.session.serializer.SignedSessionSerializer.deserialize

```{autodoc2-docstring} fastlife.middlewares.session.serializer.SignedSessionSerializer.deserialize
:parser: myst
```

````

````{py:method} serialize(data: typing.Mapping[str, typing.Any]) -> bytes
:canonical: fastlife.middlewares.session.serializer.SignedSessionSerializer.serialize

```{autodoc2-docstring} fastlife.middlewares.session.serializer.SignedSessionSerializer.serialize
:parser: myst
```

````

`````

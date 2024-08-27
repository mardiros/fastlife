# {py:mod}`fastlife.request.form`

```{py:module} fastlife.request.form
```

```{autodoc2-docstring} fastlife.request.form
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FormModel <fastlife.request.form.FormModel>`
  - ```{autodoc2-docstring} fastlife.request.form.FormModel
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`form_model <fastlife.request.form.form_model>`
  - ```{autodoc2-docstring} fastlife.request.form.form_model
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`T <fastlife.request.form.T>`
  - ```{autodoc2-docstring} fastlife.request.form.T
    :summary:
    ```
````

### API

````{py:data} T
:canonical: fastlife.request.form.T
:value: >
   'TypeVar(...)'

```{autodoc2-docstring} fastlife.request.form.T
```

````

`````{py:class} FormModel(prefix: str, model: fastlife.request.form.T, errors: typing.Mapping[str, typing.Any], is_valid: bool = False)
:canonical: fastlife.request.form.FormModel

Bases: {py:obj}`typing.Generic`\[{py:obj}`fastlife.request.form.T`\]

```{autodoc2-docstring} fastlife.request.form.FormModel
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.request.form.FormModel.__init__
```

````{py:attribute} prefix
:canonical: fastlife.request.form.FormModel.prefix
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.request.form.FormModel.prefix
```

````

````{py:attribute} model
:canonical: fastlife.request.form.FormModel.model
:type: fastlife.request.form.T
:value: >
   None

```{autodoc2-docstring} fastlife.request.form.FormModel.model
```

````

````{py:attribute} errors
:canonical: fastlife.request.form.FormModel.errors
:type: typing.Mapping[str, str]
:value: >
   None

```{autodoc2-docstring} fastlife.request.form.FormModel.errors
```

````

````{py:attribute} is_valid
:canonical: fastlife.request.form.FormModel.is_valid
:type: bool
:value: >
   None

```{autodoc2-docstring} fastlife.request.form.FormModel.is_valid
```

````

````{py:method} default(prefix: str, pydantic_type: typing.Type[fastlife.request.form.T]) -> FormModel[T]
:canonical: fastlife.request.form.FormModel.default
:classmethod:

```{autodoc2-docstring} fastlife.request.form.FormModel.default
```

````

````{py:method} edit(pydantic_type: fastlife.request.form.T) -> None
:canonical: fastlife.request.form.FormModel.edit

```{autodoc2-docstring} fastlife.request.form.FormModel.edit
```

````

````{py:property} form_data
:canonical: fastlife.request.form.FormModel.form_data
:type: typing.Mapping[str, typing.Any]

```{autodoc2-docstring} fastlife.request.form.FormModel.form_data
```

````

````{py:method} from_payload(prefix: str, pydantic_type: typing.Type[fastlife.request.form.T], data: typing.Mapping[str, typing.Any]) -> FormModel[T]
:canonical: fastlife.request.form.FormModel.from_payload
:classmethod:

```{autodoc2-docstring} fastlife.request.form.FormModel.from_payload
```

````

`````

````{py:function} form_model(cls: typing.Type[fastlife.request.form.T], name: str | None = None) -> typing.Callable[[typing.Mapping[str, typing.Any]], fastlife.request.form.FormModel[fastlife.request.form.T]]
:canonical: fastlife.request.form.form_model

```{autodoc2-docstring} fastlife.request.form.form_model
```
````

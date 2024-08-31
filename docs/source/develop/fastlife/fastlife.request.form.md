# {py:mod}`fastlife.request.form`

```{py:module} fastlife.request.form
```

```{autodoc2-docstring} fastlife.request.form
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`form_model <fastlife.request.form.form_model>`
  - ```{autodoc2-docstring} fastlife.request.form.form_model
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`T <fastlife.request.form.T>`
  - ```{autodoc2-docstring} fastlife.request.form.T
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} T
:canonical: fastlife.request.form.T
:value: >
   'TypeVar(...)'

```{autodoc2-docstring} fastlife.request.form.T
:parser: myst
```

````

````{py:function} form_model(cls: typing.Type[fastlife.request.form.T], name: str | None = None) -> typing.Callable[[typing.Mapping[str, typing.Any]], fastlife.request.form.FormModel[fastlife.request.form.T]]
:canonical: fastlife.request.form.form_model

```{autodoc2-docstring} fastlife.request.form.form_model
:parser: myst
```
````

# {py:mod}`fastlife.views.pydantic_form`

```{py:module} fastlife.views.pydantic_form
```

```{autodoc2-docstring} fastlife.views.pydantic_form
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`show_widget <fastlife.views.pydantic_form.show_widget>`
  - ```{autodoc2-docstring} fastlife.views.pydantic_form.show_widget
    :summary:
    ```
* - {py:obj}`includeme <fastlife.views.pydantic_form.includeme>`
  - ```{autodoc2-docstring} fastlife.views.pydantic_form.includeme
    :summary:
    ```
````

### API

````{py:function} show_widget(typ: str, reg: fastlife.config.registry.Registry, request: fastapi.Request, title: typing.Optional[str] = Query(None), name: typing.Optional[str] = Query(None), token: typing.Optional[str] = Query(None), removable: bool = Query(False)) -> fastapi.Response
:canonical: fastlife.views.pydantic_form.show_widget
:async:

```{autodoc2-docstring} fastlife.views.pydantic_form.show_widget
```
````

````{py:function} includeme(config: fastlife.Configurator) -> None
:canonical: fastlife.views.pydantic_form.includeme

```{autodoc2-docstring} fastlife.views.pydantic_form.includeme
```
````

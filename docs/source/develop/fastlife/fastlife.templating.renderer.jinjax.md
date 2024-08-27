# {py:mod}`fastlife.templating.renderer.jinjax`

```{py:module} fastlife.templating.renderer.jinjax
```

```{autodoc2-docstring} fastlife.templating.renderer.jinjax
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`JinjaxRenderer <fastlife.templating.renderer.jinjax.JinjaxRenderer>`
  -
* - {py:obj}`JinjaxTemplateRenderer <fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`build_searchpath <fastlife.templating.renderer.jinjax.build_searchpath>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.jinjax.build_searchpath
    :summary:
    ```
````

### API

````{py:function} build_searchpath(template_search_path: str) -> typing.Sequence[str]
:canonical: fastlife.templating.renderer.jinjax.build_searchpath

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.build_searchpath
```
````

`````{py:class} JinjaxRenderer(catalog: jinjax.catalog.Catalog, request: fastapi.Request, csrf_token_name: str, form_data_model_prefix: str, route_prefix: str)
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer

Bases: {py:obj}`fastlife.templating.renderer.abstract.AbstractTemplateRenderer`

````{py:method} build_globals() -> typing.Mapping[str, typing.Any]
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer.build_globals

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxRenderer.build_globals
```

````

````{py:method} render_template(template: str, *, globals: typing.Optional[typing.Mapping[str, typing.Any]] = None, **params: typing.Any) -> str
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer.render_template

````

````{py:method} pydantic_form(model: fastlife.request.form.FormModel[typing.Any], *, token: typing.Optional[str] = None) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer.pydantic_form

````

````{py:method} pydantic_form_field(model: typing.Type[typing.Any], *, name: str | None, token: str | None, removable: bool, field: pydantic.fields.FieldInfo | None) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer.pydantic_form_field

````

`````

`````{py:class} JinjaxTemplateRenderer(settings: fastlife.config.settings.Settings)
:canonical: fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer

Bases: {py:obj}`fastlife.templating.renderer.abstract.AbstractTemplateRendererFactory`

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.__init__
```

````{py:attribute} route_prefix
:canonical: fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.route_prefix
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.route_prefix
```

````

````{py:method} __call__(request: fastapi.Request) -> fastlife.templating.renderer.abstract.AbstractTemplateRenderer
:canonical: fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.__call__

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.__call__
```

````

`````

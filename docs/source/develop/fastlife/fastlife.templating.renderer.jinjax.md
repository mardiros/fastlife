# {py:mod}`fastlife.templating.renderer.jinjax`

```{py:module} fastlife.templating.renderer.jinjax
```

```{autodoc2-docstring} fastlife.templating.renderer.jinjax
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`InspectableCatalog <fastlife.templating.renderer.jinjax.InspectableCatalog>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.jinjax.InspectableCatalog
    :parser: myst
    :summary:
    ```
* - {py:obj}`InspectableComponent <fastlife.templating.renderer.jinjax.InspectableComponent>`
  -
* - {py:obj}`JinjaxRenderer <fastlife.templating.renderer.jinjax.JinjaxRenderer>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxRenderer
    :parser: myst
    :summary:
    ```
* - {py:obj}`JinjaxTemplateRenderer <fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`build_searchpath <fastlife.templating.renderer.jinjax.build_searchpath>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.jinjax.build_searchpath
    :parser: myst
    :summary:
    ```
* - {py:obj}`generate_docstring <fastlife.templating.renderer.jinjax.generate_docstring>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.jinjax.generate_docstring
    :parser: myst
    :summary:
    ```
````

### API

````{py:class} InspectableCatalog(*, globals: dict[str, t.Any] | None = None, filters: dict[str, t.Any] | None = None, tests: dict[str, t.Any] | None = None, extensions: list | None = None, jinja_env: jinja2.Environment | None = None, root_url: str = DEFAULT_URL_ROOT, file_ext: str | tuple[str, ...] = DEFAULT_EXTENSION, use_cache: bool = True, auto_reload: bool = True, fingerprint: bool = False)
:canonical: fastlife.templating.renderer.jinjax.InspectableCatalog

Bases: {py:obj}`jinjax.catalog.Catalog`

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.InspectableCatalog
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.InspectableCatalog.__init__
:parser: myst
```

````

```{py:class} InspectableComponent(*, name: str, prefix: str = '', url_prefix: str = '', source: str = '', mtime: float = 0, tmpl: Template | None = None, path: Path | None = None)
:canonical: fastlife.templating.renderer.jinjax.InspectableComponent

Bases: {py:obj}`jinjax.component.Component`

```

`````{py:class} JinjaxRenderer(catalog: fastlife.templating.renderer.jinjax.InspectableCatalog, request: fastapi.Request, csrf_token_name: str, form_data_model_prefix: str, route_prefix: str)
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer

Bases: {py:obj}`fastlife.templating.renderer.abstract.AbstractTemplateRenderer`

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxRenderer
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxRenderer.__init__
:parser: myst
```

````{py:method} build_globals() -> typing.Mapping[str, typing.Any]
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer.build_globals

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxRenderer.build_globals
:parser: myst
```

````

````{py:method} pydantic_form(model: fastlife.request.form.FormModel[typing.Any], *, token: typing.Optional[str] = None) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer.pydantic_form

````

````{py:method} pydantic_form_field(model: typing.Type[typing.Any], *, name: str | None, token: str | None, removable: bool, field: pydantic.fields.FieldInfo | None) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer.pydantic_form_field

````

````{py:method} render_template(template: str, *, globals: typing.Optional[typing.Mapping[str, typing.Any]] = None, **params: typing.Any) -> str
:canonical: fastlife.templating.renderer.jinjax.JinjaxRenderer.render_template

````

`````

`````{py:class} JinjaxTemplateRenderer(settings: fastlife.config.settings.Settings)
:canonical: fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer

Bases: {py:obj}`fastlife.templating.renderer.abstract.AbstractTemplateRendererFactory`

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.__init__
:parser: myst
```

````{py:method} __call__(request: fastapi.Request) -> fastlife.templating.renderer.abstract.AbstractTemplateRenderer
:canonical: fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.__call__

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.__call__
:parser: myst
```

````

````{py:attribute} route_prefix
:canonical: fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.route_prefix
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer.route_prefix
:parser: myst
```

````

`````

````{py:function} build_searchpath(template_search_path: str) -> typing.Sequence[str]
:canonical: fastlife.templating.renderer.jinjax.build_searchpath

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.build_searchpath
:parser: myst
```
````

````{py:function} generate_docstring(func_def: ast.FunctionDef, component_name: str, add_content: bool) -> str
:canonical: fastlife.templating.renderer.jinjax.generate_docstring

```{autodoc2-docstring} fastlife.templating.renderer.jinjax.generate_docstring
:parser: myst
```
````

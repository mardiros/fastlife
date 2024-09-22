# {py:mod}`fastlife.adapters.jinjax.renderer`

```{py:module} fastlife.adapters.jinjax.renderer
```

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`InspectableCatalog <fastlife.adapters.jinjax.renderer.InspectableCatalog>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableCatalog
    :parser: myst
    :summary:
    ```
* - {py:obj}`InspectableComponent <fastlife.adapters.jinjax.renderer.InspectableComponent>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableComponent
    :parser: myst
    :summary:
    ```
* - {py:obj}`JinjaxRenderer <fastlife.adapters.jinjax.renderer.JinjaxRenderer>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.JinjaxRenderer
    :parser: myst
    :summary:
    ```
* - {py:obj}`JinjaxTemplateRenderer <fastlife.adapters.jinjax.renderer.JinjaxTemplateRenderer>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.JinjaxTemplateRenderer
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`build_searchpath <fastlife.adapters.jinjax.renderer.build_searchpath>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.build_searchpath
    :parser: myst
    :summary:
    ```
* - {py:obj}`generate_docstring <fastlife.adapters.jinjax.renderer.generate_docstring>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.generate_docstring
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} InspectableCatalog(*, globals: dict[str, t.Any] | None = None, filters: dict[str, t.Any] | None = None, tests: dict[str, t.Any] | None = None, extensions: list | None = None, jinja_env: jinja2.Environment | None = None, root_url: str = DEFAULT_URL_ROOT, file_ext: str | tuple[str, ...] = DEFAULT_EXTENSION, use_cache: bool = True, auto_reload: bool = True, fingerprint: bool = False)
:canonical: fastlife.adapters.jinjax.renderer.InspectableCatalog

Bases: {py:obj}`jinjax.catalog.Catalog`

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableCatalog
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableCatalog.__init__
:parser: myst
```

````{py:method} iter_components(ignores: typing.Sequence[re.Pattern[str]] | None = None, includes: typing.Sequence[re.Pattern[str]] | None = None) -> typing.Iterator[fastlife.adapters.jinjax.renderer.InspectableComponent]
:canonical: fastlife.adapters.jinjax.renderer.InspectableCatalog.iter_components

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableCatalog.iter_components
:parser: myst
```

````

`````

`````{py:class} InspectableComponent(*, name: str, prefix: str = '', url_prefix: str = '', source: str = '', mtime: float = 0, tmpl: Template | None = None, path: Path | None = None)
:canonical: fastlife.adapters.jinjax.renderer.InspectableComponent

Bases: {py:obj}`jinjax.component.Component`

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableComponent
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableComponent.__init__
:parser: myst
```

````{py:method} as_def() -> ast.FunctionDef
:canonical: fastlife.adapters.jinjax.renderer.InspectableComponent.as_def

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableComponent.as_def
:parser: myst
```

````

````{py:method} build_docstring() -> str
:canonical: fastlife.adapters.jinjax.renderer.InspectableComponent.build_docstring

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.InspectableComponent.build_docstring
:parser: myst
```

````

`````

`````{py:class} JinjaxRenderer(catalog: fastlife.adapters.jinjax.renderer.InspectableCatalog, request: fastlife.Request)
:canonical: fastlife.adapters.jinjax.renderer.JinjaxRenderer

Bases: {py:obj}`fastlife.services.templates.AbstractTemplateRenderer`

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.JinjaxRenderer
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.JinjaxRenderer.__init__
:parser: myst
```

````{py:method} build_globals() -> typing.Mapping[str, typing.Any]
:canonical: fastlife.adapters.jinjax.renderer.JinjaxRenderer.build_globals

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.JinjaxRenderer.build_globals
:parser: myst
```

````

````{py:method} render_template(template: str, *, globals: typing.Optional[typing.Mapping[str, typing.Any]] = None, **params: typing.Any) -> str
:canonical: fastlife.adapters.jinjax.renderer.JinjaxRenderer.render_template

````

`````

`````{py:class} JinjaxTemplateRenderer(settings: fastlife.config.settings.Settings)
:canonical: fastlife.adapters.jinjax.renderer.JinjaxTemplateRenderer

Bases: {py:obj}`fastlife.services.templates.AbstractTemplateRendererFactory`

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.JinjaxTemplateRenderer
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.JinjaxTemplateRenderer.__init__
:parser: myst
```

````{py:method} __call__(request: fastlife.Request) -> fastlife.services.templates.AbstractTemplateRenderer
:canonical: fastlife.adapters.jinjax.renderer.JinjaxTemplateRenderer.__call__

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.JinjaxTemplateRenderer.__call__
:parser: myst
```

````

`````

````{py:function} build_searchpath(template_search_path: str) -> typing.Sequence[str]
:canonical: fastlife.adapters.jinjax.renderer.build_searchpath

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.build_searchpath
:parser: myst
```
````

````{py:function} generate_docstring(func_def: ast.FunctionDef, component_name: str, add_content: bool) -> str
:canonical: fastlife.adapters.jinjax.renderer.generate_docstring

```{autodoc2-docstring} fastlife.adapters.jinjax.renderer.generate_docstring
:parser: myst
```
````

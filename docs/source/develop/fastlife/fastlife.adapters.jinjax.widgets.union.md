# {py:mod}`fastlife.adapters.jinjax.widgets.union`

```{py:module} fastlife.adapters.jinjax.widgets.union
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.union
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`UnionWidget <fastlife.adapters.jinjax.widgets.union.UnionWidget>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.union.UnionWidget
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} UnionWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, value: typing.Optional[fastlife.adapters.jinjax.widgets.base.Widget[typing.Any]], error: str | None = None, children_types: typing.Sequence[typing.Type[pydantic.BaseModel]], removable: bool = False, token: str)
:canonical: fastlife.adapters.jinjax.widgets.union.UnionWidget

Bases: {py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`typing.Any`\]\]

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.union.UnionWidget
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.union.UnionWidget.__init__
:parser: myst
```

````{py:method} build_types(route_prefix: str) -> typing.Sequence[fastlife.adapters.jinjax.widgets.base.TypeWrapper]
:canonical: fastlife.adapters.jinjax.widgets.union.UnionWidget.build_types

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.union.UnionWidget.build_types
:parser: myst
```

````

````{py:method} get_template() -> str
:canonical: fastlife.adapters.jinjax.widgets.union.UnionWidget.get_template

````

````{py:method} to_html(renderer: fastlife.services.templates.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.adapters.jinjax.widgets.union.UnionWidget.to_html

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.union.UnionWidget.to_html
:parser: myst
```

````

`````

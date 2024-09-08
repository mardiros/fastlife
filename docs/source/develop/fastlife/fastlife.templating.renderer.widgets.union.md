---
orphan: true
---

# {py:mod}`fastlife.templating.renderer.widgets.union`

```{py:module} fastlife.templating.renderer.widgets.union
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.union
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`UnionWidget <fastlife.templating.renderer.widgets.union.UnionWidget>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.union.UnionWidget
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} UnionWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, value: typing.Optional[fastlife.templating.renderer.widgets.base.Widget[typing.Any]], error: str | None = None, children_types: typing.Sequence[typing.Type[pydantic.BaseModel]], removable: bool = False, token: str)
:canonical: fastlife.templating.renderer.widgets.union.UnionWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`typing.Any`\]\]

```{autodoc2-docstring} fastlife.templating.renderer.widgets.union.UnionWidget
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.union.UnionWidget.__init__
:parser: myst
```

````{py:method} get_template() -> str
:canonical: fastlife.templating.renderer.widgets.union.UnionWidget.get_template

````

````{py:method} to_html(renderer: fastlife.templating.renderer.abstract.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.widgets.union.UnionWidget.to_html

```{autodoc2-docstring} fastlife.templating.renderer.widgets.union.UnionWidget.to_html
:parser: myst
```

````

`````

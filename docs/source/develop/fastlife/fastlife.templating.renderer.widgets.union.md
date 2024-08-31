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
  -
````

### API

`````{py:class} UnionWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, value: typing.Optional[fastlife.templating.renderer.widgets.base.Widget[typing.Any]], error: str | None = None, children_types: typing.Sequence[typing.Type[pydantic.BaseModel]], token: str, removable: bool)
:canonical: fastlife.templating.renderer.widgets.union.UnionWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`typing.Any`\]\]

````{py:method} to_html(renderer: fastlife.templating.renderer.abstract.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.widgets.union.UnionWidget.to_html

```{autodoc2-docstring} fastlife.templating.renderer.widgets.union.UnionWidget.to_html
:parser: myst
```

````

`````

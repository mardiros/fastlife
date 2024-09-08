---
orphan: true
---

# {py:mod}`fastlife.templating.renderer.widgets.model`

```{py:module} fastlife.templating.renderer.widgets.model
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.model
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`ModelWidget <fastlife.templating.renderer.widgets.model.ModelWidget>`
  -
````

### API

`````{py:class} ModelWidget(name: str, *, value: typing.Sequence[fastlife.templating.renderer.widgets.base.Widget[typing.Any]], error: str | None = None, removable: bool, title: str, hint: str | None = None, aria_label: str | None = None, token: str, nested: bool)
:canonical: fastlife.templating.renderer.widgets.model.ModelWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`typing.Sequence`\[{py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`typing.Any`\]\]\]

````{py:method} get_template() -> str
:canonical: fastlife.templating.renderer.widgets.model.ModelWidget.get_template

````

````{py:method} to_html(renderer: fastlife.templating.renderer.abstract.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.widgets.model.ModelWidget.to_html

```{autodoc2-docstring} fastlife.templating.renderer.widgets.model.ModelWidget.to_html
:parser: myst
```

````

`````

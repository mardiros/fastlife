---
orphan: true
---

# {py:mod}`fastlife.adapters.jinjax.widgets.model`

```{py:module} fastlife.adapters.jinjax.widgets.model
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.model
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`ModelWidget <fastlife.adapters.jinjax.widgets.model.ModelWidget>`
  -
````

### API

`````{py:class} ModelWidget(name: str, *, value: typing.Sequence[fastlife.adapters.jinjax.widgets.base.Widget[typing.Any]], error: str | None = None, removable: bool, title: str, hint: str | None = None, aria_label: str | None = None, token: str, nested: bool)
:canonical: fastlife.adapters.jinjax.widgets.model.ModelWidget

Bases: {py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`typing.Sequence`\[{py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`typing.Any`\]\]\]

````{py:method} get_template() -> str
:canonical: fastlife.adapters.jinjax.widgets.model.ModelWidget.get_template

````

````{py:method} to_html(renderer: fastlife.services.templates.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.adapters.jinjax.widgets.model.ModelWidget.to_html

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.model.ModelWidget.to_html
:parser: myst
```

````

`````

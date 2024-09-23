---
orphan: true
---

# {py:mod}`fastlife.adapters.jinjax.widgets.sequence`

```{py:module} fastlife.adapters.jinjax.widgets.sequence
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.sequence
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SequenceWidget <fastlife.adapters.jinjax.widgets.sequence.SequenceWidget>`
  -
````

### API

`````{py:class} SequenceWidget(name: str, *, title: str | None, hint: str | None = None, aria_label: str | None = None, value: typing.Sequence[fastlife.adapters.jinjax.widgets.base.Widget[typing.Any]] | None, error: str | None = None, item_type: typing.Type[typing.Any], token: str, removable: bool)
:canonical: fastlife.adapters.jinjax.widgets.sequence.SequenceWidget

Bases: {py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`typing.Sequence`\[{py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`typing.Any`\]\]\]

````{py:method} get_template() -> str
:canonical: fastlife.adapters.jinjax.widgets.sequence.SequenceWidget.get_template

````

````{py:method} to_html(renderer: fastlife.services.templates.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.adapters.jinjax.widgets.sequence.SequenceWidget.to_html

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.sequence.SequenceWidget.to_html
:parser: myst
```

````

`````

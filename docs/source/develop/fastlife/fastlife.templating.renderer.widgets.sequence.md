---
orphan: true
---

# {py:mod}`fastlife.templating.renderer.widgets.sequence`

```{py:module} fastlife.templating.renderer.widgets.sequence
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.sequence
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SequenceWidget <fastlife.templating.renderer.widgets.sequence.SequenceWidget>`
  -
````

### API

`````{py:class} SequenceWidget(name: str, *, title: str | None, hint: str | None = None, aria_label: str | None = None, value: typing.Sequence[fastlife.templating.renderer.widgets.base.Widget[typing.Any]] | None, error: str | None = None, item_type: typing.Type[typing.Any], token: str, removable: bool)
:canonical: fastlife.templating.renderer.widgets.sequence.SequenceWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`typing.Sequence`\[{py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`typing.Any`\]\]\]

````{py:method} to_html(renderer: fastlife.templating.renderer.abstract.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.widgets.sequence.SequenceWidget.to_html

```{autodoc2-docstring} fastlife.templating.renderer.widgets.sequence.SequenceWidget.to_html
:parser: myst
```

````

`````

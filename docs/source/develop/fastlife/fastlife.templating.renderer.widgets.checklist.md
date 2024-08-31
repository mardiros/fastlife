---
orphan: true
---

# {py:mod}`fastlife.templating.renderer.widgets.checklist`

```{py:module} fastlife.templating.renderer.widgets.checklist
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.checklist
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Checkable <fastlife.templating.renderer.widgets.checklist.Checkable>`
  -
* - {py:obj}`ChecklistWidget <fastlife.templating.renderer.widgets.checklist.ChecklistWidget>`
  -
````

### API

```{py:class} Checkable(/, **data: typing.Any)
:canonical: fastlife.templating.renderer.widgets.checklist.Checkable

Bases: {py:obj}`pydantic.BaseModel`

```

```{py:class} ChecklistWidget(name: str, *, title: str | None, hint: str | None = None, aria_label: str | None = None, value: typing.Sequence[fastlife.templating.renderer.widgets.checklist.Checkable], error: str | None = None, token: str, removable: bool)
:canonical: fastlife.templating.renderer.widgets.checklist.ChecklistWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`typing.Sequence`\[{py:obj}`fastlife.templating.renderer.widgets.checklist.Checkable`\]\]

```

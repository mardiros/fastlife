# {py:mod}`fastlife.adapters.jinjax.widgets.checklist`

```{py:module} fastlife.adapters.jinjax.widgets.checklist
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.checklist
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Checkable <fastlife.adapters.jinjax.widgets.checklist.Checkable>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.checklist.Checkable
    :parser: myst
    :summary:
    ```
* - {py:obj}`ChecklistWidget <fastlife.adapters.jinjax.widgets.checklist.ChecklistWidget>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.checklist.ChecklistWidget
    :parser: myst
    :summary:
    ```
````

### API

````{py:class} Checkable(/, **data: typing.Any)
:canonical: fastlife.adapters.jinjax.widgets.checklist.Checkable

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.checklist.Checkable
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.checklist.Checkable.__init__
:parser: myst
```

````

`````{py:class} ChecklistWidget(name: str, *, title: str | None, hint: str | None = None, aria_label: str | None = None, value: typing.Sequence[fastlife.adapters.jinjax.widgets.checklist.Checkable], error: str | None = None, token: str, removable: bool)
:canonical: fastlife.adapters.jinjax.widgets.checklist.ChecklistWidget

Bases: {py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`typing.Sequence`\[{py:obj}`fastlife.adapters.jinjax.widgets.checklist.Checkable`\]\]

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.checklist.ChecklistWidget
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.checklist.ChecklistWidget.__init__
:parser: myst
```

````{py:method} get_template() -> str
:canonical: fastlife.adapters.jinjax.widgets.checklist.ChecklistWidget.get_template

````

`````

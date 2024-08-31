---
orphan: true
---

# {py:mod}`fastlife.templating.renderer.widgets.dropdown`

```{py:module} fastlife.templating.renderer.widgets.dropdown
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.dropdown
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`DropDownWidget <fastlife.templating.renderer.widgets.dropdown.DropDownWidget>`
  -
````

### API

```{py:class} DropDownWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, value: typing.Optional[str] = None, error: str | None = None, options: typing.Sequence[typing.Tuple[str, str]] | typing.Sequence[str], removable: bool = False, token: typing.Optional[str] = None)
:canonical: fastlife.templating.renderer.widgets.dropdown.DropDownWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`str`\]

```

---
orphan: true
---

# {py:mod}`fastlife.adapters.jinjax.widgets.text`

```{py:module} fastlife.adapters.jinjax.widgets.text
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.text
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TextWidget <fastlife.adapters.jinjax.widgets.text.TextWidget>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.text.TextWidget
    :parser: myst
    :summary:
    ```
* - {py:obj}`TextareaWidget <fastlife.adapters.jinjax.widgets.text.TextareaWidget>`
  - ```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.text.TextareaWidget
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} TextWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, placeholder: typing.Optional[str] = None, error: str | None = None, value: str = '', input_type: str = 'text', removable: bool = False, token: str)
:canonical: fastlife.adapters.jinjax.widgets.text.TextWidget

Bases: {py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`str`\]

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.text.TextWidget
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.text.TextWidget.__init__
:parser: myst
```

````{py:method} get_template() -> str
:canonical: fastlife.adapters.jinjax.widgets.text.TextWidget.get_template

````

`````

`````{py:class} TextareaWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, placeholder: typing.Optional[str] = None, error: str | None = None, value: str = '', removable: bool = False, token: str)
:canonical: fastlife.adapters.jinjax.widgets.text.TextareaWidget

Bases: {py:obj}`fastlife.adapters.jinjax.widgets.base.Widget`\[{py:obj}`str`\]

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.text.TextareaWidget
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.adapters.jinjax.widgets.text.TextareaWidget.__init__
:parser: myst
```

````{py:method} get_template() -> str
:canonical: fastlife.adapters.jinjax.widgets.text.TextareaWidget.get_template

````

`````

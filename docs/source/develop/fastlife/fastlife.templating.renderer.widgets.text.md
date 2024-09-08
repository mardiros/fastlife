---
orphan: true
---

# {py:mod}`fastlife.templating.renderer.widgets.text`

```{py:module} fastlife.templating.renderer.widgets.text
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.text
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TextWidget <fastlife.templating.renderer.widgets.text.TextWidget>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.text.TextWidget
    :parser: myst
    :summary:
    ```
* - {py:obj}`TextareaWidget <fastlife.templating.renderer.widgets.text.TextareaWidget>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.text.TextareaWidget
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} TextWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, placeholder: typing.Optional[str] = None, error: str | None = None, value: str = '', input_type: str = 'text', removable: bool = False, token: str)
:canonical: fastlife.templating.renderer.widgets.text.TextWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`str`\]

```{autodoc2-docstring} fastlife.templating.renderer.widgets.text.TextWidget
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.text.TextWidget.__init__
:parser: myst
```

````{py:method} get_template() -> str
:canonical: fastlife.templating.renderer.widgets.text.TextWidget.get_template

````

`````

`````{py:class} TextareaWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, placeholder: typing.Optional[str] = None, error: str | None = None, value: str = '', removable: bool = False, token: str)
:canonical: fastlife.templating.renderer.widgets.text.TextareaWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`str`\]

```{autodoc2-docstring} fastlife.templating.renderer.widgets.text.TextareaWidget
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.text.TextareaWidget.__init__
:parser: myst
```

````{py:method} get_template() -> str
:canonical: fastlife.templating.renderer.widgets.text.TextareaWidget.get_template

````

`````

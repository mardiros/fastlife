# {py:mod}`fastlife.templating.renderer.widgets.text`

```{py:module} fastlife.templating.renderer.widgets.text
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.text
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TextWidget <fastlife.templating.renderer.widgets.text.TextWidget>`
  -
* - {py:obj}`TextareaWidget <fastlife.templating.renderer.widgets.text.TextareaWidget>`
  -
````

### API

`````{py:class} TextWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, placeholder: typing.Optional[str] = None, error: str | None = None, removable: bool = False, value: str = '', token: typing.Optional[str] = None, input_type: str = 'text')
:canonical: fastlife.templating.renderer.widgets.text.TextWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`str`\]

````{py:method} get_template() -> str
:canonical: fastlife.templating.renderer.widgets.text.TextWidget.get_template

```{autodoc2-docstring} fastlife.templating.renderer.widgets.text.TextWidget.get_template
```

````

`````

`````{py:class} TextareaWidget(name: str, *, title: typing.Optional[str], hint: typing.Optional[str] = None, aria_label: typing.Optional[str] = None, placeholder: typing.Optional[str] = None, error: str | None = None, removable: bool = False, value: str = '', token: typing.Optional[str] = None)
:canonical: fastlife.templating.renderer.widgets.text.TextareaWidget

Bases: {py:obj}`fastlife.templating.renderer.widgets.base.Widget`\[{py:obj}`str`\]

````{py:method} get_template() -> str
:canonical: fastlife.templating.renderer.widgets.text.TextareaWidget.get_template

```{autodoc2-docstring} fastlife.templating.renderer.widgets.text.TextareaWidget.get_template
```

````

`````

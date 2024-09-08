---
orphan: true
---

# {py:mod}`fastlife.templating.renderer.widgets.base`

```{py:module} fastlife.templating.renderer.widgets.base
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TypeWrapper <fastlife.templating.renderer.widgets.base.TypeWrapper>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper
    :parser: myst
    :summary:
    ```
* - {py:obj}`Widget <fastlife.templating.renderer.widgets.base.Widget>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} TypeWrapper(typ: typing.Type[typing.Any], route_prefix: str, name: str, token: str, title: str | None = None)
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.__init__
:parser: myst
```

````{py:property} fullname
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper.fullname
:type: str

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.fullname
:parser: myst
```

````

````{py:property} id
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper.id
:type: str

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.id
:parser: myst
```

````

````{py:property} params
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper.params
:type: typing.Mapping[str, str]

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.params
:parser: myst
```

````

````{py:property} url
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper.url
:type: str

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.url
:parser: myst
```

````

`````

`````{py:class} Widget(name: str, *, value: fastlife.templating.renderer.widgets.base.T | None = None, error: str | None = None, title: str | None = None, hint: str | None = None, token: str | None = None, aria_label: str | None = None, removable: bool = False)
:canonical: fastlife.templating.renderer.widgets.base.Widget

Bases: {py:obj}`abc.ABC`, {py:obj}`typing.Generic`\[{py:obj}`fastlife.templating.renderer.widgets.base.T`\]

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.__init__
:parser: myst
```

````{py:attribute} aria_label
:canonical: fastlife.templating.renderer.widgets.base.Widget.aria_label
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.aria_label
:parser: myst
```

````

````{py:method} get_template() -> str
:canonical: fastlife.templating.renderer.widgets.base.Widget.get_template
:abstractmethod:

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.get_template
:parser: myst
```

````

````{py:attribute} hint
:canonical: fastlife.templating.renderer.widgets.base.Widget.hint
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.hint
:parser: myst
```

````

````{py:attribute} name
:canonical: fastlife.templating.renderer.widgets.base.Widget.name
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.name
:parser: myst
```

````

````{py:attribute} removable
:canonical: fastlife.templating.renderer.widgets.base.Widget.removable
:type: bool
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.removable
:parser: myst
```

````

````{py:attribute} title
:canonical: fastlife.templating.renderer.widgets.base.Widget.title
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.title
:parser: myst
```

````

````{py:method} to_html(renderer: fastlife.templating.renderer.abstract.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.widgets.base.Widget.to_html

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.to_html
:parser: myst
```

````

````{py:attribute} token
:canonical: fastlife.templating.renderer.widgets.base.Widget.token
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.token
:parser: myst
```

````

````{py:attribute} value
:canonical: fastlife.templating.renderer.widgets.base.Widget.value
:type: fastlife.templating.renderer.widgets.base.T | None
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.value
:parser: myst
```

````

`````

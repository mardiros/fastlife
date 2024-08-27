# {py:mod}`fastlife.templating.renderer.widgets.base`

```{py:module} fastlife.templating.renderer.widgets.base
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Widget <fastlife.templating.renderer.widgets.base.Widget>`
  -
* - {py:obj}`TypeWrapper <fastlife.templating.renderer.widgets.base.TypeWrapper>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`get_title <fastlife.templating.renderer.widgets.base.get_title>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.get_title
    :summary:
    ```
* - {py:obj}`_get_fullname <fastlife.templating.renderer.widgets.base._get_fullname>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.base._get_fullname
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`T <fastlife.templating.renderer.widgets.base.T>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.T
    :summary:
    ```
````

### API

````{py:data} T
:canonical: fastlife.templating.renderer.widgets.base.T
:value: >
   'TypeVar(...)'

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.T
```

````

````{py:function} get_title(typ: typing.Type[typing.Any]) -> str
:canonical: fastlife.templating.renderer.widgets.base.get_title

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.get_title
```
````

`````{py:class} Widget(name: str, *, value: fastlife.templating.renderer.widgets.base.T | None = None, error: str | None = None, title: str | None = None, hint: str | None = None, token: str | None = None, aria_label: str | None = None, removable: bool = False)
:canonical: fastlife.templating.renderer.widgets.base.Widget

Bases: {py:obj}`abc.ABC`, {py:obj}`typing.Generic`\[{py:obj}`fastlife.templating.renderer.widgets.base.T`\]

````{py:attribute} name
:canonical: fastlife.templating.renderer.widgets.base.Widget.name
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.name
```

````

````{py:attribute} title
:canonical: fastlife.templating.renderer.widgets.base.Widget.title
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.title
```

````

````{py:attribute} hint
:canonical: fastlife.templating.renderer.widgets.base.Widget.hint
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.hint
```

````

````{py:attribute} aria_label
:canonical: fastlife.templating.renderer.widgets.base.Widget.aria_label
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.aria_label
```

````

````{py:attribute} token
:canonical: fastlife.templating.renderer.widgets.base.Widget.token
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.token
```

````

````{py:attribute} removable
:canonical: fastlife.templating.renderer.widgets.base.Widget.removable
:type: bool
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.removable
```

````

````{py:method} get_template() -> str
:canonical: fastlife.templating.renderer.widgets.base.Widget.get_template
:abstractmethod:

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.get_template
```

````

````{py:method} to_html(renderer: fastlife.templating.renderer.abstract.AbstractTemplateRenderer) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.widgets.base.Widget.to_html

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.to_html
```

````

`````

````{py:function} _get_fullname(typ: typing.Type[typing.Any]) -> str
:canonical: fastlife.templating.renderer.widgets.base._get_fullname

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base._get_fullname
```
````

`````{py:class} TypeWrapper(typ: typing.Type[typing.Any], route_prefix: str, name: str, token: str, title: str | None = None)
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.__init__
```

````{py:property} fullname
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper.fullname
:type: str

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.fullname
```

````

````{py:property} id
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper.id
:type: str

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.id
```

````

````{py:property} params
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper.params
:type: typing.Mapping[str, str]

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.params
```

````

````{py:property} url
:canonical: fastlife.templating.renderer.widgets.base.TypeWrapper.url
:type: str

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.TypeWrapper.url
```

````

`````

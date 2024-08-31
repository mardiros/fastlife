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

* - {py:obj}`Widget <fastlife.templating.renderer.widgets.base.Widget>`
  -
````

### API

`````{py:class} Widget(name: str, *, value: fastlife.templating.renderer.widgets.base.T | None = None, error: str | None = None, title: str | None = None, hint: str | None = None, token: str | None = None, aria_label: str | None = None, removable: bool = False)
:canonical: fastlife.templating.renderer.widgets.base.Widget

Bases: {py:obj}`abc.ABC`, {py:obj}`typing.Generic`\[{py:obj}`fastlife.templating.renderer.widgets.base.T`\]

````{py:attribute} aria_label
:canonical: fastlife.templating.renderer.widgets.base.Widget.aria_label
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.widgets.base.Widget.aria_label
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

`````

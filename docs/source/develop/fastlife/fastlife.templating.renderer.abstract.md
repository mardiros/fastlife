# {py:mod}`fastlife.templating.renderer.abstract`

```{py:module} fastlife.templating.renderer.abstract
```

```{autodoc2-docstring} fastlife.templating.renderer.abstract
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AbstractTemplateRenderer <fastlife.templating.renderer.abstract.AbstractTemplateRenderer>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRenderer
    :summary:
    ```
* - {py:obj}`AbstractTemplateRendererFactory <fastlife.templating.renderer.abstract.AbstractTemplateRendererFactory>`
  - ```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRendererFactory
    :summary:
    ```
````

### API

`````{py:class} AbstractTemplateRenderer
:canonical: fastlife.templating.renderer.abstract.AbstractTemplateRenderer

Bases: {py:obj}`abc.ABC`

```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRenderer
```

````{py:attribute} route_prefix
:canonical: fastlife.templating.renderer.abstract.AbstractTemplateRenderer.route_prefix
:type: str
:value: >
   None

```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRenderer.route_prefix
```

````

````{py:method} render_template(template: str, *, globals: typing.Optional[typing.Mapping[str, typing.Any]] = None, **params: typing.Any) -> str
:canonical: fastlife.templating.renderer.abstract.AbstractTemplateRenderer.render_template
:abstractmethod:

```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRenderer.render_template
```

````

````{py:method} pydantic_form(model: fastlife.request.form.FormModel[typing.Any], *, token: typing.Optional[str] = None) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.abstract.AbstractTemplateRenderer.pydantic_form
:abstractmethod:

```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRenderer.pydantic_form
```

````

````{py:method} pydantic_form_field(model: typing.Type[typing.Any], *, name: str | None, token: str | None, removable: bool, field: pydantic.fields.FieldInfo | None) -> markupsafe.Markup
:canonical: fastlife.templating.renderer.abstract.AbstractTemplateRenderer.pydantic_form_field
:abstractmethod:

```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRenderer.pydantic_form_field
```

````

`````

`````{py:class} AbstractTemplateRendererFactory
:canonical: fastlife.templating.renderer.abstract.AbstractTemplateRendererFactory

Bases: {py:obj}`abc.ABC`

```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRendererFactory
```

````{py:method} __call__(request: fastapi.Request) -> fastlife.templating.renderer.abstract.AbstractTemplateRenderer
:canonical: fastlife.templating.renderer.abstract.AbstractTemplateRendererFactory.__call__
:abstractmethod:

```{autodoc2-docstring} fastlife.templating.renderer.abstract.AbstractTemplateRendererFactory.__call__
```

````

`````

# {py:mod}`fastlife.services.templates`

```{py:module} fastlife.services.templates
```

```{autodoc2-docstring} fastlife.services.templates
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AbstractTemplateRenderer <fastlife.services.templates.AbstractTemplateRenderer>`
  - ```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRenderer
    :parser: myst
    :summary:
    ```
* - {py:obj}`AbstractTemplateRendererFactory <fastlife.services.templates.AbstractTemplateRendererFactory>`
  - ```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRendererFactory
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} AbstractTemplateRenderer(request: fastlife.Request)
:canonical: fastlife.services.templates.AbstractTemplateRenderer

Bases: {py:obj}`abc.ABC`

```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRenderer
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRenderer.__init__
:parser: myst
```

````{py:method} render(template: str, *, status_code: int = 200, content_type: str = 'text/html', globals: typing.Mapping[str, typing.Any] | None = None, params: fastlife.services.templates.TemplateParams, _create_csrf_token: typing.Callable[..., str] = create_csrf_token) -> fastlife.Response
:canonical: fastlife.services.templates.AbstractTemplateRenderer.render

```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRenderer.render
:parser: myst
```

````

````{py:method} render_template(template: str, *, globals: typing.Mapping[str, typing.Any] | None = None, **params: typing.Any) -> str
:canonical: fastlife.services.templates.AbstractTemplateRenderer.render_template
:abstractmethod:

```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRenderer.render_template
:parser: myst
```

````

````{py:attribute} request
:canonical: fastlife.services.templates.AbstractTemplateRenderer.request
:type: fastlife.Request
:value: >
   None

```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRenderer.request
:parser: myst
```

````

````{py:property} route_prefix
:canonical: fastlife.services.templates.AbstractTemplateRenderer.route_prefix
:type: str

```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRenderer.route_prefix
:parser: myst
```

````

`````

`````{py:class} AbstractTemplateRendererFactory
:canonical: fastlife.services.templates.AbstractTemplateRendererFactory

Bases: {py:obj}`abc.ABC`

```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRendererFactory
:parser: myst
```

````{py:method} __call__(request: fastlife.Request) -> fastlife.services.templates.AbstractTemplateRenderer
:canonical: fastlife.services.templates.AbstractTemplateRendererFactory.__call__
:abstractmethod:

```{autodoc2-docstring} fastlife.services.templates.AbstractTemplateRendererFactory.__call__
:parser: myst
```

````

`````

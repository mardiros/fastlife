# Working with templates

In fastlife, templates are declarable in multiple way,
in the [boostrap with poetry](#bootstrap-with-poetry), we learn
the simplest way to use a template, using the `template` attributes
of the {func}`@view_config decorator <fastlife.config.views.view_config>`

```python
from fastlife import view_config

@view_config("hello_world", "/",  template="HelloWorld.jinja")
def hello_world() -> dict[str, str]:
    return {}
```

But, there is an other option to achieve the same result that is a bit more verbose
but more flexible.

```python
from fastlife import Response
from fastlife.templates import Template, template

@view_config("hello_world", "/")
def hello_world(
    template: Annotated[Template, template("HelloWorld.jinja")],
) -> Response:
    return template()
```

In this example, we use a FastAPI dependency that will render the HelloWorld.jinja
template file.

:::{tip}
This method is very usefull in two situation:

- We have to choose between multiple templates in the view depending on other parameter.
- We want to call the view from another vue using composition.
  :::

From a testing point of view rendering template inside the view,
we are not able to tests the rendering parameters of the view anymore.
And we are forced to tests with the {attr}`WebTestClient
<fastlife.testing.testclient.WebTestClient>`.

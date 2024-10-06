# Handling forms

Fastlife provide a library to bind form with pydantic models directly.

There is a set of {term}`widgets <widget>` available and that is completly
overridable using an annotation.

:::{admonition} wip
This section describe pydantic_form using JinjaX directly.

There is no abstraction made to use a pydantic_form using another template engine
at the moment until it is stabilized.

Some widget are not completly ended, especially sequence manipulation.
:::

## Quickstart

To starts handling form, we will use the helloworld example from the
[bootstrap with poetry](#bootstrap-with-poetry) and add
a simple form in the page to say hello, has a classic example.

We will first update the template to add a form in it:

```bash
cat << 'EOF' > src/myapp/templates/HelloWorld.jinja
{# def person #}
<html>
    <body>
      <H1>Hello {{ person.model.nick|default("World") }}!</H1>
      <Form method="post">
        {{ pydantic_form(person) }}
        <Button>Submit</Button>
      </Form>
    </body>
<html>
EOF
```

In jinjax, we have to declare the definition of the variables of the templates,
The annotation are optional and ommited here.

The function
:meth:`pydantic_form <fastlife.adapters.jinjax.renderer.JinjaxRenderer.pydantic_form>`
invoked here will render the template content, but not the
{jinjax:component}`Form` itself to let the choice on how the form behave.
It also don't render submit buttons to give the control of it too.

:::{tip}
The {jinjax:component}`Form` will automatically inject a CSRF token and the
app always create a cookie to prevent CSRF attacks.
:::

Now we need to add update the view because we have a new parameter person
that need to be defined. The person is a {class}`fastlife.request.form.FormModel`
that wrap a pydantic BaseModel in order to provide errors management.

```bash
cat << 'EOF' > src/myapp/views.py
from typing import Annotated

from fastlife import view_config, TemplateParams
from pydantic import BaseModel
from fastlife.request.form import FormModel, form_model


class Person(BaseModel):
    nick: str


@view_config("home", "/", methods=["GET", "POST"], template="HelloWorld.jinja")
async def hello_world(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> TemplateParams:
    return {"person": person}

EOF
```

Now, if you run the app and start a browser, you see the form with one field to the
the nick name.

You can fill the nick and submit the form to test that it works, but, we are
going to test it via the test client intead.

```bash
cat << 'EOF' >> tests/test_views.py

def test_hello_form(client: WebTestClient):
    page = client.get("/")
    page.form.set("person.nick", "Bob")
    page = page.form.submit()
    assert page.html.h1.text == "Hello Bob!"
EOF
```

The {class}`WebTestClient <fastlife.testing.client.WebTestClient>` can handle
forms. In our case we, set the field and submit the form, then verify that
the page has been updated.

Run the tests to verify it works.

## Customizing the form.

The display of the fields can be simply enhanced by filled out pydantic properties
properly.

- The `title` of the `Field` is converted to the label of the field.
- The `description` of the `Field` is converted to a hint of the field.
- The `examples[0]` of the `Field` is converted to a placeholder of the field.

###

```bash
cat << 'EOF' > src/myapp/views.py
from typing import Annotated

from fastlife import view_config, TemplateParams
from pydantic import BaseModel, Field
from fastlife.request.form import FormModel, form_model


class Person(BaseModel):
    nick: str = Field(
        title="Nickname", description="Avatar from the 80s", examples=["RadRacer"]
    )


@view_config("home", "/", methods=["GET", "POST"], template="HelloWorld.jinja")
async def hello_world(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> TemplateParams:
    return {"person": person}

EOF
```

:::{tip}
Run it and you will see a raw html without any css.
The recipe [add css stylesheet](#add-css-stylesheet) can fix the problem.
:::


### Example of form using different widgets

```python
from typing import Annotated
from uuid import UUID, uuid1

from fastlife.adapters.jinjax.widgets.base import Widget
from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget
from fastlife.adapters.jinjax.widgets.text import TextareaWidget
from pydantic import BaseModel, Field


class MyWidget(Widget[str]):
    def get_template(self) -> str:
        return "MyWidget.jinja"


class PetForm(BaseModel):
    id: Annotated[UUID, HiddenWidget] = Field(default=uuid1)
    nick: Annotated[str, MyWidget] = Field(title="Pet's Name")
    description: Annotated[str, TextareaWidget] = Field(title="Pet's hobbies")
    favorite_toy: str = Field(title="Favorite Toy")
    magic_power: bool = Field(title="Has Magic Power")
```

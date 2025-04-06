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

from fastlife import view_config
from pydantic import BaseModel
from fastlife.request.form import FormModel, form_model


class Person(BaseModel):
    nick: str


class HelloWorld(JinjaXTemplate):
    template = """
    <html>
        <body>
          <H1>Hello {{ person.model.nick|default("World") }}!</H1>
          <Form method="post">
            {{ pydantic_form(person) }}
            <Button>Submit</Button>
          </Form>
        </body>
    <html>
    """
    person: FormModel[Person]


@view_config("home", "/", methods=["GET", "POST"])
async def hello_world(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> HelloWorld:
    return HelloWorld(person=person)

EOF
```

:::{tip}
Usually, with jinjax, we have to declare the definition of the variables in templates,
but using the JinjaXTemplate object, the definition is automatically creating with
the attributes of the class. `person` in our example.
:::

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

### Customize fields display

The display of the fields can be simply enhanced by filled out pydantic properties
properly.

- The `title` of the `Field` is converted to the label of the field.
- The `description` of the `Field` is converted to a hint of the field.
- The `examples[0]` of the `Field` is converted to a placeholder of the field.

```bash
cat << 'EOF' > src/myapp/views.py
from typing import Annotated

from fastlife import view_config
from pydantic import BaseModel, Field
from fastlife.request.form import FormModel, form_model


class Person(BaseModel):
    nick: str = Field(
        title="Nickname", description="Avatar from the 80s", examples=["RadRacer"]
    )


class HelloWorld(JinjaXTemplate):
    template = """
    <html>
        <body>
          <H1>Hello {{ person.model.nick|default("World") }}!</H1>
          <Form method="post">
            {{ pydantic_form(person) }}
            <Button>Submit</Button>
          </Form>
        </body>
    <html>
    """
    person: FormModel[Person]


@view_config("home", "/", methods=["GET", "POST"], template="HelloWorld.jinja")
async def hello_world(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> HelloWorld:
    return HelloWorld(person=person)

EOF
```

:::{tip}
Run it and you will see a raw html without any css.
The recipe [add css stylesheet](#add-css-stylesheet) can fix the problem.
:::

### Widgets per type

Python builtin types and Pydantic models have their own widget. For example,
boolean use {jinjax:component}`checkboxes <Checkbox>`, enum types use
{jinjax:component}`select <Select>`.

It is also possible to create widgets and use an annotation in order to get
a full control of the rendering. We just need to inherits a class from
{class}`fastlife.adapters.jinjax.widgets.base.Widget`

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
    id: Annotated[UUID, CustomWidget(HiddenWidget)] = Field(default=uuid1)
    nick: Annotated[str, CustomWidget(MyWidget)] = Field(title="Pet's Name")
    description: Annotated[str, CustomWidget(TextareaWidget)] = Field(title="Pet's hobbies")
    favorite_toy: str = Field(title="Favorite Toy")
    magic_power: bool = Field(title="Has Magic Power")
```

## Do some HTMX.

We can update the form to do the hello in {term}`HTMX`

```bash
cat << 'EOF' > src/myapp/templates/HelloWorld.jinja
{# def person #}
<html>
    <head>
    <script src="https://unpkg.com/htmx.org@2.0.4" integrity="sha384-HGfztofotfshcF7+8n44JQL2oJmowVChPTg48S+jvZoztPfvwD79OC/LTtG6dMp+" crossorigin="anonymous"></script>
    </head>
    <body>
      <H1 id="hello-world">Hello {{ person.model.nick|default("World") }}!</H1>
      <Form hx-post="{{ request.url_for('hx-hello')}}" hx-target="#hello-world">
        {{ pydantic_form(person) }}
        <Button>Submit</Button>
      </Form>
    </body>
<html>
EOF
```

Now we have a form that post on a route named `hx-hello` and its response,
will replace the inner html part of the element with the id "hello-world".

lets add this view.

```
cat << 'EOF' > src/myapp/views.py
from typing import Annotated

from fastlife import view_config, Response
from pydantic import BaseModel, Field
from fastlife.request.form import FormModel, form_model


class Person(BaseModel):
    nick: str = Field(
        title="Nickname", description="Avatar from the 80s", examples=["RadRacer"]
    )


class HelloWorld(JinjaXTemplate):
    template = """
    <html>
        <body>
          <H1>Hello {{ person.model.nick|default("World") }}!</H1>
          <Form method="post">
            {{ pydantic_form(person) }}
            <Button>Submit</Button>
          </Form>
        </body>
    <html>
    """
    person: FormModel[Person]


@view_config("home", "/", methods=["GET"], template="HelloWorld.jinja")
async def hello_world(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> HelloWorld:
    return HelloWorld(person=person)


@view_config("hx-hello", "/hx-hello", methods=["POST"])
async def hx_hello_world(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> Response:
    return Response(f"Hello {person.model.nick}!")

EOF
```

In the real world, we may reuse the same route for the GET and the POST,
event with HTMX, and do a embed the response in different layout depending
it is a HTMX request or not. The alternative is to use the hx-target
attribute. All of this is well documented at HTMX website to lean more
about HTMX at https://htmx.org/.

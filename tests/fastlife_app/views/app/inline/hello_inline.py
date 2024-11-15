"""A dummy view to test inline templates."""

from typing import Annotated, Literal

from pydantic import Field

from fastlife import view_config
from fastlife.request.form import FormModel, form_model
from fastlife.templates.inline import InlineTemplate
from tests.fastlife_app.models import Person


class HelloInline(InlineTemplate):
    template = """
    <Layout>
      <H1>Hello {{ person.nick|default("World") }}!</H1>
      <Form :method="method">
        <Input name="person.nick"
            label="Name"
            aria_label="First name and last name, or surname"
            />
        <Button aria_label="submit">Submit</Button>
      </Form>
    </Layout>
    """
    renderer = ".jinja"
    person: Annotated[Person | None, "You"] = Field(default=None)
    method: Annotated[Literal["get", "post"], "Form method"] = "post"


@view_config("hello-inline", "/inline/hello-world", methods=["GET"])
async def hello_inline(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> HelloInline:
    return HelloInline(person=person.model)

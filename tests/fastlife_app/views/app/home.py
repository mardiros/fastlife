from typing import Annotated

from fastlife import view_config
from fastlife.domain.model.template import JinjaXTemplate
from fastlife.request.form import FormModel, form_model
from fastlife.request.request import Request
from tests.fastlife_app.models import Account, Group, Person


class HelloWorld(JinjaXTemplate):
    template = """<HelloWorld :person="person" />"""
    person: Person


@view_config("home", "/", methods=["GET", "POST"])
async def hello_world(
    person: Annotated[FormModel[Person], form_model(Person, "person")],
) -> HelloWorld:
    return HelloWorld(person=person.model)


class AutoForm(JinjaXTemplate):
    template = """
    <Layout>
      <div class="max-w-screen-lg mx-auto px-5 bg-white min-h-sceen">
        <Form hx-post="">
          {{ pydantic_form(model=model) }}
          <Button>Submit</Button>
        </Form>
      </div>
    </Layout>
    """
    model: FormModel[Account]


@view_config("autoform", "/autoform", methods=["GET", "POST"])
async def autoform(
    request: Request,
    account: Annotated[FormModel[Account], form_model(Account)],
) -> AutoForm:
    request.add_renderer_globals(
        all_groups=[
            Group(name="admin"),
            Group(name="editor"),
            Group(name="moderator"),
        ]
    )
    return AutoForm(model=account)

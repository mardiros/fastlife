from typing import Annotated, Any

from fastapi import Path, Response
from pydantic import BaseModel

from fastlife import view_config
from fastlife.adapters.fastapi.form_data import MappingFormData
from fastlife.adapters.fastapi.request import Request
from fastlife.adapters.xcomponent.registry import x_component
from fastlife.domain.model.form import FormModel
from fastlife.domain.model.template import XTemplate
from fastlife.shared_utils.resolver import resolve


@x_component()
def TestForm(model: BaseModel) -> str:
    return """
    <Layout>
      <div class="max-w-(--breakpoint-lg) mx-auto px-5 bg-white min-h-sceen">
        <Form method="post">
          { globals.pydantic_form(model) }
          <Button>Submit</Button>
        </Form>
      </div>
    </Layout>
    """


class TestFormPage(XTemplate):
    template = "<TestForm model={model} />"
    model: FormModel[Any]


@view_config("form", "/form/{type}", methods=["GET", "POST"])
async def testform(
    request: Request,
    type: Annotated[str, Path],
    data: MappingFormData,
) -> TestFormPage | Response:
    cls = resolve(f"tests.fastlife_app.views.app.forms.{type}:Form")
    if request.method == "POST":
        model = FormModel[BaseModel].from_payload(
            request.registry.settings.form_data_model_prefix, cls, data
        )
        return Response(
            model.model.model_dump_json(), headers={"Content-Type": "application/json"}
        )
    model = FormModel[Any].default(
        request.registry.settings.form_data_model_prefix, cls
    )
    return TestFormPage(model=model)


@view_config("formcomplex", "/form-complex/{type}", methods=["GET", "POST"])
async def testcomplexform(
    request: Request,
    type: Annotated[str, Path],
    data: MappingFormData,
) -> TestFormPage | Response:
    cls = resolve(f"tests.fastlife_app.views.app.forms.complex.{type}:Form")
    if request.method == "POST":
        model = FormModel[BaseModel].from_payload(
            request.registry.settings.form_data_model_prefix, cls, data
        )
        return Response(
            model.model.model_dump_json(), headers={"Content-Type": "application/json"}
        )
    model = FormModel[Any].default(
        request.registry.settings.form_data_model_prefix, cls
    )
    return TestFormPage(model=model)

from typing import Annotated, Any

from fastapi import Path, Response
from pydantic import BaseModel

from fastlife import Configurator, Template, configure, template
from fastlife.request.form import FormModel
from fastlife.request.form_data import MappingFormData
from fastlife.request.request import Request
from fastlife.shared_utils.resolver import resolve


async def testform(
    request: Request,
    type: Annotated[str, Path],
    data: MappingFormData,
    template: Annotated[Template, template("TestForm.jinja")],
) -> Response:
    cls = resolve(f"tests.fastlife_app.views.forms.{type}:Form")
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
    return template(model=model)


@configure
def includeme(config: Configurator):
    config.add_route("form", "/form/{type}", testform, methods=["GET", "POST"])

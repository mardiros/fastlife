from typing import Annotated, Any

from fastapi import Path, Response
from pydantic import BaseModel

from fastlife import Configurator, Template, configure, template
from fastlife.configurator.route_handler import FastlifeRequest
from fastlife.request.form_data import MappingFormData
from fastlife.request.model_result import ModelResult
from fastlife.shared_utils.resolver import resolve


async def testform(
    request: FastlifeRequest,
    type: Annotated[str, Path],
    data: MappingFormData,
    template: Annotated[Template, template("TestForm")],
) -> Response:
    cls = resolve(f"tests.fastlife_app.views.forms.{type}:Form")
    if request.method == "POST":
        model = ModelResult[BaseModel].from_payload(
            request.registry.settings.form_data_model_prefix, cls, data
        )
        return Response(
            model.model.model_dump_json(), headers={"Content-Type": "application/json"}
        )
    model = ModelResult[Any].default(
        request.registry.settings.form_data_model_prefix, cls
    )
    return template(model=model)


@configure
def includeme(config: Configurator):
    config.add_route("form", "/form/{type}", testform, methods=["GET", "POST"])

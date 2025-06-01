"""
Template renderer based on XComponent.

More template engine can be registered using the configurator method
{meth}`add_renderer <fastlife.config.configurator.GenericConfigurator.add_renderer>`
"""

from typing import Any

from fastlife import Request
from fastlife.domain.model.template import InlineTemplate
from fastlife.service.templates import (
    AbstractTemplateRenderer,
    AbstractTemplateRendererFactory,
)
from fastlife.settings import Settings
from fastlife.shared_utils.resolver import resolve

from .catalog import catalog


class XTemplateRenderer(AbstractTemplateRenderer):
    """
    An object that will be initialized by an AbstractTemplateRendererFactory,
    passing the request to process.
    """

    request: Request
    """Associated request that needs a response."""

    def __init__(self, globals: dict[str, Any], request: Request) -> None:
        self.request = request
        self.globals: dict[str, Any] = {**globals}

    @property
    def route_prefix(self) -> str:
        """Used to buid pydantic form widget that do ajax requests."""
        return self.request.registry.settings.fastlife_route_prefix

    def render_template(self, template: InlineTemplate) -> str:
        """
        Render an inline template.

        :param template: the template to render.
        :return: The template rendering result.
        """
        params = template.model_dump()
        return catalog.render(
            template.template,
            globals=self.globals,
            **params,
        )


class XRendererFactory(AbstractTemplateRendererFactory):
    """
    The template render factory.
    """

    def __init__(self, settings: "Settings") -> None:
        self.globals = resolve(settings.jinjax_global_catalog_class)().model_dump()

    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        """
        While processing an HTTP Request, a renderer object is created giving
        isolated context per request.

        :param Request: the HTTP Request to process.
        :return: The renderer object that will process that request.
        """
        return XTemplateRenderer(globals=self.globals, request=request)

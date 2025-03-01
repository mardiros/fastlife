"""
Base class to of the template renderer.

Fastlife comes with {class}`fastlife.adapters.jinjax.renderer.JinjaxEngine`,
the rendering engine.

More template engine can be registered using the configurator method
{meth}`add_renderer <fastlife.config.configurator.GenericConfigurator.add_renderer>`
"""

import abc
from collections.abc import Mapping
from typing import Any

from fastlife import Request, Response
from fastlife.domain.model.template import InlineTemplate


class AbstractTemplateRenderer(abc.ABC):
    """
    An object that will be initialized by an AbstractTemplateRendererFactory,
    passing the request to process.
    """

    request: Request
    """Associated request that needs a response."""

    def __init__(self, request: Request) -> None:
        self.request = request
        self.globals: dict[str, Any] = {}

    @property
    def route_prefix(self) -> str:
        """Used to buid pydantic form widget that do ajax requests."""
        return self.request.registry.settings.fastlife_route_prefix

    def render(
        self,
        template: str,
        *,
        status_code: int = 200,
        content_type: str = "text/html",
        globals: Mapping[str, Any] | None = None,
        params: InlineTemplate,
    ) -> Response:
        """
        Render the template and build the HTTP Response.
        """
        request = self.request
        if globals:
            self.globals.update(globals)
        data = self.render_template(params)
        resp = Response(
            data, status_code=status_code, headers={"Content-Type": content_type}
        )
        resp.set_cookie(
            request.csrf_token.name,
            request.csrf_token.value,
            httponly=True,
            secure=request.url.scheme == "https",
            samesite="strict",
            max_age=60 * 15,
        )
        return resp

    @abc.abstractmethod
    def render_template(self, template: InlineTemplate) -> str:
        """
        Render an inline template.

        :param template: the template to render.
        :return: The template rendering result.
        """


class AbstractTemplateRendererFactory(abc.ABC):
    """
    The template render factory.
    """

    @abc.abstractmethod
    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        """
        While processing an HTTP Request, a renderer object is created giving
        isolated context per request.

        :param Request: the HTTP Request to process.
        :return: The renderer object that will process that request.
        """

"""
Base class to of the template renderer.

Fastlife comes with {class}`fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer`,
the rendering engine, it can be overriden from the setting
:attr:`fastlife.config.settings.Settings.template_renderer_class`.

In that case, those base classes have to be implemented.

"""

import abc
from typing import Any, Callable, Mapping

from fastlife import Request, Response
from fastlife.security.csrf import create_csrf_token

TemplateParams = Mapping[str, Any]


class AbstractTemplateRenderer(abc.ABC):
    """
    An object that will be initialized by an AbstractTemplateRendererFactory,
    passing the request to process.
    """

    request: Request
    """Associated request that needs a response."""

    def __init__(self, request: Request) -> None:
        self.request = request

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
        params: TemplateParams,
        _create_csrf_token: Callable[..., str] = create_csrf_token,
    ) -> Response:
        """
        Render the template and build the HTTP Response.
        """
        request = self.request
        reg = request.registry
        request.scope[reg.settings.csrf_token_name] = (
            request.cookies.get(reg.settings.csrf_token_name) or _create_csrf_token()
        )
        data = self.render_template(template, **params)
        resp = Response(
            data, status_code=status_code, headers={"Content-Type": content_type}
        )
        resp.set_cookie(
            reg.settings.csrf_token_name,
            request.scope[reg.settings.csrf_token_name],
            secure=request.url.scheme == "https",
            samesite="strict",
            max_age=60 * 15,
        )
        return resp

    @abc.abstractmethod
    def render_template(
        self,
        template: str,
        *,
        globals: Mapping[str, Any] | None = None,
        **params: Any,
    ) -> str:
        """
        Render the given template with the given params.

        While rendering templates, the globals parameter is keps by the instantiated
        renderer and sent to every rendering made by the request.
        This is used by the pydantic form method that will render other templates
        for the request.
        In traditional frameworks, only one template is rendered containing the whole
        pages. But, while rendering a pydantic form, every field is rendered in its
        distinct template. The template renderer keep the globals and git it back
        to every templates. This can be used to fillout options in a select without
        performing an ajax request for example.

        :param template: name of the template to render.
        :param globals: some variable that will be passed to all rendered templates.
        :param params: paramaters that are limited to the main rendered templates.
        :return: The template rendering result.
        """


class AbstractTemplateRendererFactory(abc.ABC):
    """
    The template render factory.

    The implementation of this class is found using the settings
    :attr:`fastlife.config.settings.Settings.template_renderer_class`.
    """

    @abc.abstractmethod
    def __call__(self, request: Request) -> AbstractTemplateRenderer:
        """
        While processing an HTTP Request, a renderer object is created giving
        isolated context per request.

        :param Request: the HTTP Request to process.
        :return: The renderer object that will process that request.
        """

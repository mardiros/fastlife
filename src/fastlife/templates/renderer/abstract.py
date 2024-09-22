"""
Base class to of the template renderer.

Fastlife comes with :class:`fastlife.templating.renderer.jinjax.JinjaxTemplateRenderer`,
the rendering engine, it can be overriden from the setting
:attr:`fastlife.config.settings.Settings.template_renderer_class`.

In that case, those base classes have to be implemented.

"""

import abc
from typing import Any, Callable, Mapping, Optional, Type

from markupsafe import Markup
from pydantic.fields import FieldInfo

from fastlife import Request, Response
from fastlife.request.form import FormModel
from fastlife.security.csrf import create_csrf_token


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
        content_type: str = "text/html",
        globals: Optional[Mapping[str, Any]] = None,
        params: Mapping[str, Any],
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
        resp = Response(data, headers={"Content-Type": content_type})
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
        globals: Optional[Mapping[str, Any]] = None,
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

    @abc.abstractmethod
    def pydantic_form(
        self, model: FormModel[Any], *, token: Optional[str] = None
    ) -> Markup:
        """
        Render an http form from a given model.

        Because template post may be give back to users with errors,
        the model is wrap in an object containing initial model, or validated model
        and a set of errors.

        this function is used inside the template directly. And it will not render the
        <form> tag so the action/httpx post is not handled byu the method..
        Somethinging like this:

        ::

            <Form action="" method="post">
                {{ pydantic_form(model) }}
            </Form>


        :param model: model to render.
        :param token: a random string that can be passed for testing purpose.
        """
        ...

    @abc.abstractmethod
    def pydantic_form_field(
        self,
        model: Type[Any],
        *,
        name: str | None,
        token: str | None,
        removable: bool,
        field: FieldInfo | None,
    ) -> Markup:
        """
        Render a field of a model inside a pydantic_form.

        Models that contains field of type Union, for instance may have
        many types of children and the form have a user interaction to choose
        which sub type to select. When the user choose the type, the sub model is
        rendered using this helper under the hood.
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
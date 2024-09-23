"""
Bind template to the view in order to build an html response.
"""

from typing import Any, Callable

from fastapi import Depends, Response

from fastlife.request import Request
from fastlife.security.csrf import create_csrf_token

Template = Callable[..., Response]
"""Type to annotate a FastAPI depency injection."""

TemplateEngine = Callable[[Request], Template]


def get_template(template: str, *, content_type: str = "text/html") -> TemplateEngine:
    """
    Return a closure to render the given template.

    :param template: path to template to render.
    :param content_type: response ``Content-Type`` header.
    """

    def render_template(
        request: Request,
        *,
        _create_csrf_token: Callable[..., str] = create_csrf_token,
    ) -> Template:
        reg = request.registry

        def parametrizer(**kwargs: Any) -> Response:
            return reg.get_renderer(template)(request).render(
                template, content_type=content_type, params=kwargs
            )

        return parametrizer

    return render_template


def template(template_path: str) -> Template:
    """
    Return a FastAPI dependency template engine ready to render the template.


    :param template_path: path to template to render by the engine setup in the regitry.
    :return: A callable accepting kwargs to pass as the context, returning a string.
    """
    return Depends(get_template(template_path))

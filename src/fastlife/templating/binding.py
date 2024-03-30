from typing import Any, Callable

from fastapi import Depends, Request, Response

from fastlife.configurator.registry import Registry
from fastlife.security.csrf import create_csrf_token

Template = Callable[..., Response]
TemplateEngine = Callable[["Registry", Request], Template]


def get_template(template: str, *, content_type: str = "text/html") -> TemplateEngine:
    def render_template(
        reg: "Registry",
        request: Request,
        *,
        _create_csrf_token: Callable[..., str] = create_csrf_token,
    ) -> Template:
        def parametrizer(**kwargs: Any) -> Response:
            request.scope[reg.settings.csrf_token_name] = (
                request.cookies.get(reg.settings.csrf_token_name)
                or _create_csrf_token()
            )
            data = reg.renderer(request).render_template(template, **kwargs)
            resp = Response(data, headers={"Content-Type": content_type})
            resp.set_cookie(
                reg.settings.csrf_token_name,
                request.scope[reg.settings.csrf_token_name],
                secure=request.url.scheme == "https",
                samesite="strict",
                max_age=60 * 15,
            )
            return resp

        return parametrizer

    return render_template


def template(template_path: str) -> Template:
    return Depends(get_template(template_path))

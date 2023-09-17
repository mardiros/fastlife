from typing import Any, Callable, Coroutine

from fastapi import Depends, Request, Response

from fastlife.configurator.registry import Registry
from fastlife.security.csrf import create_csrf_token

TemplateEngineHandler = Coroutine[Any, Any, Response]
Template = Callable[..., TemplateEngineHandler]
TemplateEngine = Callable[[Registry, Request], Template]


def get_template(template: str, *, content_type: str = "text/html") -> TemplateEngine:
    def render_template(
        reg: Registry,
        request: Request,
        *,
        _create_csrf_token: Callable[..., str] = create_csrf_token,
    ) -> Template:
        async def parametrizer(**kwargs: Any) -> Response:
            data = await reg.renderer.render_page(request, template, **kwargs)
            resp = Response(data, headers={"Content-Type": content_type})
            resp.set_cookie(
                "csrf_token",
                request.cookies.get("csrf_token") or _create_csrf_token(),
                secure=request.url.scheme == "https",
                samesite="strict",
                max_age=60 * 15,
            )
            return resp

        return parametrizer

    return render_template


def template(template_path: str) -> Template:
    return Depends(get_template(template_path))

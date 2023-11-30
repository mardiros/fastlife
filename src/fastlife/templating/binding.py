from typing import Any, Callable, Coroutine

from fastapi import Depends, Request, Response

from fastlife.configurator.registry import Registry
from fastlife.security.csrf import create_csrf_token

TemplateEngineHandler = Coroutine[Any, Any, Response]
Template = Callable[..., TemplateEngineHandler]
TemplateEngine = Callable[["Registry", Request], Template]


def get_page_template(
    template: str, *, content_type: str = "text/html"
) -> TemplateEngine:
    def render_template(
        reg: "Registry",
        request: Request,
        *,
        _create_csrf_token: Callable[..., str] = create_csrf_token,
    ) -> Template:
        async def parametrizer(**kwargs: Any) -> Response:
            request.scope[reg.settings.csrf_token_name] = (
                request.cookies.get(reg.settings.csrf_token_name)
                or _create_csrf_token()
            )
            data = await reg.renderer.render_page(request, template, **kwargs)
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


def get_template(
    template: str, *, content_type: str = "text/html"
) -> Callable[["Registry"], Template]:
    def render_template(reg: "Registry") -> Template:
        async def parametrizer(**kwargs: Any) -> Response:
            data = await reg.renderer.render_template(template, **kwargs)
            resp = Response(data, headers={"Content-Type": content_type})
            return resp

        return parametrizer

    return render_template


def template(template_path: str, page: bool = True) -> Template:
    return Depends(
        get_page_template(template_path) if page else get_template(template_path)
    )

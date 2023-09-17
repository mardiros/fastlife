from typing import Any, Callable, Coroutine

from fastapi import Depends, Response

from fastlife.configurator.registry import Registry

TemplateEngineHandler = Coroutine[Any, Any, Response]
Template = Callable[..., TemplateEngineHandler]
TemplateEngine = Callable[[Registry], Template]


def get_template(template: str, *, content_type: str = "text/html") -> TemplateEngine:
    def render_template(app: Registry) -> Template:
        async def parametrizer(**kwargs: Any) -> Response:
            data = await app.renderer.render_template(template, **kwargs)
            return Response(data, headers={"Content-Type": content_type})

        return parametrizer

    return render_template


def template(template_path: str) -> Template:
    return Depends(get_template(template_path))

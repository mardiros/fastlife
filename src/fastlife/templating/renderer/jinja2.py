from typing import Any, AsyncGenerator, Callable, Mapping, Optional, Sequence, Type

from fastapi import Request
from jinja2 import Environment, FileSystemLoader, Template
from markupsafe import Markup

from fastlife.configurator.settings import Settings
from fastlife.shared_utils.resolver import resolve_path

from .abstract import AbstractTemplateRenderer
from .widgets.factory import WidgetFactory


def build_searchpath(template_search_path: str) -> Sequence[str]:
    searchpath: list[str] = []
    paths = template_search_path.split(",")

    for path in paths:
        if ":" in path:
            searchpath.append(resolve_path(path))
        else:
            searchpath.append(path)
    return searchpath


class Jinja2TemplateRenderer(AbstractTemplateRenderer):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.route_prefix = settings.fastlife_route_prefix
        self.env = Environment(
            loader=FileSystemLoader(build_searchpath(settings.template_search_path)),
            enable_async=True,
        )
        self.form_data_model_prefix = settings.form_data_model_prefix
        self.csrf_token_name = settings.csrf_token_name

    def _get_template(self, template: str, **kwargs: Any) -> Template:
        return self.env.get_template(
            template,
            globals={**kwargs},
        )

    def get_csrf_token(self, request: Request) -> Callable[..., str]:
        def get_csrf_token() -> str:
            return request.scope.get(self.csrf_token_name, "")

        return get_csrf_token

    async def _render_block(self, gen_blocks: AsyncGenerator[str, None]) -> str:
        # the typing of Jinja2 async is wrong. It says there is Iterator[str]
        # insead of Asyngenerator[str, None]
        blocks: list[str] = []
        async for value in gen_blocks:
            blocks.append(value)
        return self.env.concat(blocks)  # type: ignore

    async def render_page(self, request: Request, template: str, **kwargs: Any) -> str:
        """
        Render the the template to build a full page or only a block, in case of
        htmx request containing a HX-Target.
        """
        tpl = self._get_template(
            template,
            request=request,
            get_csrf_token_name=lambda: self.csrf_token_name,
            get_csrf_token=self.get_csrf_token(request),
            pydantic_form=self.pydantic_form,
        )
        if "HX-Target" in request.headers:
            block_name = request.headers["HX-Target"]
            # We render the hx-target as a Jinja2 block of the page,
            # we use low lever functions here to build only whats we need.
            # Fist, we need to push the macros in the context has it is done in the
            # base.jinja2 for compatibility.
            macros = self._get_template("globals.jinja2", request=request)
            ctx = tpl.new_context(kwargs)
            render_macros = macros.root_render_func(ctx)
            # the typing of Jinja2 async is wrong here
            gen_blocks = await self._render_block(render_macros)  # type: ignore
            # Now we build the block without the layout.
            render_block = tpl.blocks[block_name]
            gen_blocks = render_block(ctx)  # type: ignore
            return await self._render_block(gen_blocks)  # type: ignore
        else:
            # we render the full page
            ret = await tpl.render_async(**kwargs)
        return ret

    async def render_template(self, template: str, **kwargs: Any) -> str:
        tpl = self._get_template(
            template,
            pydantic_form=self.pydantic_form,
        )
        ret = await tpl.render_async(**kwargs)
        return ret

    async def pydantic_form(
        self,
        model: Type[Any],
        form_data: Optional[Mapping[str, Any]] = None,
        name: Optional[str] = None,
        token: Optional[str] = None,
        removable: bool = False,
    ) -> Markup:
        return await WidgetFactory(self, token).get_markup(
            model,
            form_data or {},
            prefix=(name or self.form_data_model_prefix),
            removable=removable,
        )

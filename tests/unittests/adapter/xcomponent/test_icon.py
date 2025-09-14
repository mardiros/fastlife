from fastlife.domain.model.template import InlineTemplate
from fastlife.service.templates import AbstractTemplateRenderer


def test_icon(renderer: AbstractTemplateRenderer):
    class MyIcon(InlineTemplate):
        template = "<Icon name='fire'/>"

    assert renderer.render_template(MyIcon()).startswith(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
    )


def test_icon_missing(renderer: AbstractTemplateRenderer):
    class MyIcon(InlineTemplate):
        template = "<Icon name='does not exists'/>"

    assert renderer.render_template(MyIcon()) == ""

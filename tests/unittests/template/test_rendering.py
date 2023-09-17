from pathlib import Path
from fastlife.template.jinja2 import Jinja2TemplateRenderer, build_searchpath

template_path = str(Path(__file__).parent / "jinja2")


def test_build_searchpath():
    path_list = build_searchpath("fastlife:templates,/tmp")
    path = str(
        (
            Path(__file__).parent.parent.parent.parent / "src" / "fastlife" / "templates"
        ).resolve()
    )
    assert path_list == [path, "/tmp"]


async def test_jinja2_renderer():
    renderer = Jinja2TemplateRenderer(template_path)
    page = await renderer.render_template("hello_world.jinja2", title="say hello")
    assert "<title>say hello</title>" in page
    assert "<h1>Hello World!</h1>" in page

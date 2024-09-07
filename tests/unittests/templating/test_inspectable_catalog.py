import re

from fastlife.config.settings import Settings
from fastlife.templating.renderer.jinjax import JinjaxTemplateRenderer


def test_jinjax_template():
    renderer = JinjaxTemplateRenderer(Settings())
    for component in renderer.catalog.iter_components(
        ignores=[re.compile(r"^[^A]"), re.compile(r"P"), re.compile(r"icons\..*\..*")]
    ):
        print(component)
        print(component.build_docstring())

    assert False

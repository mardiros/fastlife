import re

import pytest

from fastlife.config.settings import Settings
from fastlife.templating.renderer.jinjax import (
    InspectableComponent,
    JinjaxTemplateRenderer,
    has_content,
)


@pytest.mark.parametrize(
    "content,expected",
    [
        pytest.param("", False, id="no content"),
        pytest.param("blabla {{- content -}} blabla ", True, id="has {{- content -}}"),
        pytest.param("blabla {{ content }} blabla ", True, id="has {{ content }}"),
        pytest.param("blabla {{content}} blabla ", True, id="has {{content}}"),
        pytest.param(
            "blabla {# {{ content }} #} blabla ", False, id="has commented content"
        ),
        pytest.param(
            "blabla {# {{ content }} #} blabla {{ content }}",
            True,
            id="has commented content and content",
        ),
    ],
)
def test_has_content(content: str, expected: bool):
    assert has_content(content) is expected


def test_jinjax_template():
    renderer = JinjaxTemplateRenderer(Settings())
    components: list[InspectableComponent] = []
    for component in renderer.catalog.iter_components(ignores=[re.compile(r"^[^A]")]):
        components.append(component)
    assert len(components) == 1
    docstring = components[0].build_docstring()
    assert (
        docstring
        == """\
.. jinjax:component:: A(href: str,\
 hx_target: str = '#maincontent',\
 hx_select: str | None = None,\
 hx_swap: str = 'innerHTML show:body:top',\
 hx_push_url: bool = True,\
 disable_htmx: bool = False,\
 content: Any)

    Create html `<a>` node with htmx support by default.
    The `hx-get` parameter is set with the href directly unless the
    `disabled-htmx` attribute has been set.

    :param href: target link
    :param hx_target:
    :param hx_select:
    :param hx_swap:
    :param hx_push_url:
    :param disable_htmx:
    :param content: child none
"""
    )

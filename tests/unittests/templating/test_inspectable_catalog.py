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


def test_jinjax_template_ignores():
    renderer = JinjaxTemplateRenderer(Settings())
    components: list[InspectableComponent] = []
    for component in renderer.catalog.iter_components(ignores=[re.compile(r"^[^A]")]):
        components.append(component)
    assert len(components) == 1
    docstring = components[0].build_docstring()
    assert (
        docstring
        == """\
.. jinjax:component:: A(href: str, \
id: str | None = None, \
hx_target: str = '#maincontent', \
hx_select: str | None = None, \
hx_swap: str = 'innerHTML show:body:top', \
hx_push_url: bool = True, \
disable_htmx: bool = False, \
content: Any)

    Create html ``<a>`` node with htmx support by default.
    The `hx-get` parameter is set with the href directly unless the
    `disabled-htmx` attribute has been set.

    :param href: target link.
    :param id: unique identifier of the element.
    :param hx_target: target the element for swapping than the one issuing the AJAX \
request.
    :param hx_select: select the content swapped from response of the AJAX request.
    :param hx_swap: specify how the response will be swapped in relative to the target \
of an AJAX request.
    :param hx_push_url: replace the browser url with the link.
    :param disable_htmx: do not add any `hx-*` attibute to the link.
    :param content: child node.
"""
    )


def test_jinjax_template_includes():
    renderer = JinjaxTemplateRenderer(Settings())
    components: list[InspectableComponent] = []
    for component in renderer.catalog.iter_components(
        includes=[re.compile(r"^pydantic_form\.Widget$")]
    ):
        components.append(component)
    assert len(components) == 1
    docstring = components[0].build_docstring()
    assert (
        docstring
        == """\
.. jinjax:component:: pydantic_form.Widget(widget: \
fastlife.templating.renderer.widgets.base.Widget, content: Any)

    Base component for widget

    :param widget: widget to display.
    :param content: child node.
"""
    )


def test_jinjax_template_render_no_params():
    renderer = JinjaxTemplateRenderer(Settings())
    components: list[InspectableComponent] = []
    for component in renderer.catalog.iter_components(
        includes=[re.compile(r"^CsrfToken$")]
    ):
        components.append(component)
    assert len(components) == 1
    docstring = components[0].build_docstring()
    assert (
        docstring
        == """\
.. jinjax:component:: CsrfToken()

    a :jinjax:component:`Hidden` field automaticaly injected in every
    :jinjax:component:`Form` to protect against CSRF Attacks.
"""
    )


def test_jinjax_template_render_codeblock():
    renderer = JinjaxTemplateRenderer(Settings())
    components: list[InspectableComponent] = []
    for component in renderer.catalog.iter_components(
        includes=[re.compile(r"^Details$")]
    ):
        components.append(component)
    assert len(components) == 1
    docstring = components[0].build_docstring()
    assert (
        docstring
        == """\
.. jinjax:component:: Details(id: str | None = None, open: bool = True, content: Any)

    Produce a ``<details>`` html node in order to create a collapsible box.

    .. code-block:: html

      <Details>
        <Summary :id="my-summary">
          <H3 :class="H3_SUMMARY_CLASS">A title</H3>
        </Summary>
        <div>
          Some content
        </div>
      </Details>

    :param id: unique identifier of the element.
    :param open: open/close state.
    :param content: child node.
"""
    )

"""Render template using templates containing python f-string like format."""

from typing import Any

from fastlife import Configurator, Request
from fastlife.service.templates import (
    AbstractTemplateRenderer,
    AbstractTemplateRendererFactory,
)
from tests.unittests.adapter.jinjax.test_inline import InlineTemplate
from tests.unittests.conftest import pytest


class DummyTemplateRendererFactory(AbstractTemplateRendererFactory):  # type: ignore
    def __call__(self, request: Request) -> AbstractTemplateRenderer[Any]:
        raise NotImplementedError


class GString(InlineTemplate):
    pass


class DummyGStringRendererFactory(AbstractTemplateRendererFactory[GString]):
    def __call__(self, request: Request) -> AbstractTemplateRenderer[Any]:
        raise NotImplementedError


def test_add_renderer_typing_error(conf: Configurator):
    with pytest.raises(RuntimeError) as exc:
        conf.add_renderer(DummyTemplateRendererFactory())
    assert (
        str(exc.value) == "Renderer DummyTemplateRendererFactory does not declate T "
        "in AbstractTemplateRendererFactory[T] type annotations."
    )


def test_add_renderer_typing_ok(conf: Configurator):
    obj = DummyGStringRendererFactory()
    conf.add_renderer(obj)
    assert conf.registry.get_renderer(GString()) is obj

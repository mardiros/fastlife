import pytest

from fastlife import XTemplate
from fastlife.adapters.xcomponent.renderer import XRendererFactory
from fastlife.domain.model.template import InlineTemplate
from fastlife.service.registry import DefaultRegistry


class DummyTemplate(XTemplate):
    pass


class DummyUnregisteredTemplate(InlineTemplate):
    pass


def test_get_renderer(dummy_registry: DefaultRegistry):
    dummy_registry.renderers[  # type: ignore
        XTemplate
    ] = XRendererFactory(dummy_registry.settings, {})
    assert (
        dummy_registry.get_renderer(DummyTemplate()).__class__.__qualname__
        == "XRendererFactory"
    )


def test_get_renderer_unregistered(dummy_registry: DefaultRegistry):
    with pytest.raises(RuntimeError) as ctx:
        dummy_registry.get_renderer(DummyUnregisteredTemplate())
    assert str(ctx.value) == (
        "No renderer registered for template DummyUnregisteredTemplate"
    )

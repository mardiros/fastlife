import pytest

from fastlife.config.registry import DefaultRegistry


def test_get_renderer(dummy_registry: DefaultRegistry):
    assert (
        dummy_registry.get_renderer(".jinja").__class__.__qualname__
        == "JinjaxEngine"
    )


def test_get_renderer_unregitered(dummy_registry: DefaultRegistry):
    with pytest.raises(RuntimeError) as ctx:
        dummy_registry.get_renderer(".mako")
    assert str(ctx.value) == "No renderer registered for template .mako"

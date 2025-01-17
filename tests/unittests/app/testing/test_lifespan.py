from tests.unittests.app.conftest import MyConfigurator, WebTestClient


def test_lifespan(configurator: MyConfigurator, client: WebTestClient):
    assert configurator.registry.running is False
    with client:
        assert configurator.registry.running is True

    assert configurator.registry.running is False

from fastlife.testing import WebTestClient


def test_show_widget_builtins_str(client: WebTestClient):
    resp = client.get("/icons")
    assert resp.status_code == 200

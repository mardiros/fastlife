from fastlife.testing import WebTestClient


def test_show_icons_respond_200(client: WebTestClient):
    resp = client.get("/icons")
    assert resp.status_code == 200

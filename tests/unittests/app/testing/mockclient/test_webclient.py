from multidict import MultiDict

from fastlife.testing.testclient import WebTestClient


def test_get(client: WebTestClient):
    r = client.get("/yolo")
    assert r.form._formdata == MultiDict(  # type: ignore
        [("origin", "/yolo")],
    )


def test_delete(client: WebTestClient):
    r = client.delete("/yolo/1")
    assert r.status_code == 303
    assert r.headers["location"] == "/yolo/1/deleted"


def test_post(client: WebTestClient):
    r = client.post("/", MultiDict([("a", "A")]))
    assert r.form._formdata == MultiDict(  # type: ignore
        [("a", "A"), ("origin", "/")],
    )

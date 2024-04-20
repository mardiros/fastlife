from multidict import MultiDict

from fastlife.testing.testclient import WebTestClient


def test_get(client: WebTestClient):
    r = client.get("/yolo")
    assert r.form._formdata == MultiDict(  # type: ignore
        [("origin", "/yolo")],
    )


def test_post(client: WebTestClient):
    r = client.post("/", MultiDict([("a", "A")]))
    assert r.form._formdata == MultiDict(  # type: ignore
        [("a", "A"), ("origin", "/")],
    )

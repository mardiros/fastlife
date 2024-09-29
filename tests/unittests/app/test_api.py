import textwrap

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def apiclient(app: FastAPI):
    return TestClient(app, headers={"Authorization": "Bearer abc"})


def test_api_call(apiclient: TestClient):
    resp = apiclient.get("/api")
    assert resp.json() == {
        "version": "1.0",
        "build": "856f241",
    }


def test_resource_config_crud(apiclient: TestClient):
    foos = apiclient.get("/api/foos")
    assert foos.json() == []

    foos = apiclient.post("/api/foos", json={"name": "bob"})
    assert foos.json() == {"message": "Ok"}

    foos = apiclient.get("/api/foos")
    assert foos.json() == [{"name": "bob"}]

    foos = apiclient.post("/api/foos", json={"name": "alice"})
    foos = apiclient.get("/api/foos")
    assert foos.json() == [{"name": "bob"}, {"name": "alice"}]

    foos = apiclient.patch("/api/foos")
    assert foos.json() == {"detail": "Method Not Allowed"}

    foos = apiclient.patch("/api/foos/bob", json={"name": "bobby"})
    assert foos.json() == {"message": "Ok"}

    foos = apiclient.get("/api/foos/bobby")
    assert foos.json() == {"name": "bobby"}


def test_401(app: FastAPI):
    apiclient = TestClient(app, headers={})
    resp = apiclient.get("/api/foos")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Authentication required"}


def test_403(app: FastAPI):
    apiclient = TestClient(app, headers={"Authorization": "Bearer foobar"})
    resp = apiclient.get("/api/foos")
    assert resp.status_code == 403
    assert resp.json() == {"detail": "Access denied to this resource"}


def test_openapi(apiclient: TestClient):
    resp = apiclient.get("/openapi.json")
    response = resp.json()
    assert set(response.keys()) == {"paths", "info", "components", "openapi", "tags"}

    assert response["info"] == {
        "description": textwrap.dedent(
            """
            In a unit test suite, a dummy is a simple placeholder object used to
            satisfy the parameter requirements of a method or function but isn't
            actively used in the test.

            Its primary role is to avoid null or undefined values when a method
            expects an argument, but the argument itself is irrelevant to the
            test being performed.

            For example, if a function requires multiple parameters and you're
            only interested in testing the behavior of one of them, you
            can use a **dummy** for the others to focus on the aspect you're testing.

            Unlike **mocks** or **stubs**, a **dummy doesn't have any behavior
            or interactions** it's just there to fulfill the method's signature.
            """
        ),
        "summary": "API for dummies",
        "title": "Dummy API",
        "version": "4.2",
    }
    assert response["openapi"] == "3.1.0"
    assert set(response["paths"].keys()) == {
        "/api",
        "/api/foos",
        "/api/foos/{name}",
    }

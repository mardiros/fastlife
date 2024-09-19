import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def apiclient(app: FastAPI):
    return TestClient(app)


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


def test_openapi(apiclient: TestClient):
    resp = apiclient.get("/openapi.json")
    response = resp.json()
    assert set(response.keys()) == {"paths", "info", "components", "openapi"}

    assert response["info"] == {"title": "Dummy API", "version": "4.2"}
    assert response["openapi"] == "3.1.0"
    assert set(response["paths"].keys()) == {
        "/api",
        "/api/dummies",
        "/api/foos",
        "/api/foos/{name}",
    }

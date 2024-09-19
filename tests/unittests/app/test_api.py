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


def test_openapi(apiclient: TestClient):
    resp = apiclient.get("/openapi.json")
    assert resp.json() == {
        "components": {
            "schemas": {
                "Dummy": {
                    "properties": {"name": {"title": "Name", "type": "string"}},
                    "required": ["name"],
                    "title": "Dummy",
                    "type": "object",
                },
                "Info": {
                    "properties": {
                        "build": {"title": "Build", "type": "string"},
                        "version": {"title": "Version", "type": "string"},
                    },
                    "required": ["version", "build"],
                    "title": "Info",
                    "type": "object",
                },
            },
            "securitySchemes": {
                "OAuth2PasswordBearer": {
                    "flows": {"password": {"scopes": {}, "tokenUrl": "http://token"}},
                    "type": "oauth2",
                }
            },
        },
        "info": {"title": "Dummy API", "version": "4.2"},
        "openapi": "3.1.0",
        "paths": {
            "/api": {
                "get": {
                    "description": "Return application build information",
                    "operationId": "home",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Info"}
                                }
                            },
                            "description": "Build Info",
                        }
                    },
                    "summary": "Retrieve Build Information",
                    "tags": ["monitoring"],
                }
            },
            "/api/dummies": {
                "get": {
                    "description": "Fetch a list of dummies.",
                    "operationId": "list_dummies",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {"$ref": "#/components/schemas/Dummy"},
                                        "title": "Response List Dummies",
                                        "type": "array",
                                    }
                                }
                            },
                            "description": "Dummies collection",
                        }
                    },
                    "security": [{"OAuth2PasswordBearer": []}],
                    "summary": "API For Dummies",
                    "tags": ["dummies"],
                }
            },
        },
    }

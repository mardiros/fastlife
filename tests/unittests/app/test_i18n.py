import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastlife.testing import WebTestClient


@pytest.fixture
def apiclient(app: FastAPI):
    return TestClient(app)


def test_hello_i18n(client: WebTestClient):
    resp = client.get("/fr/hello")
    assert resp.html.h1.text == "Salut tout le monde !"


def test_i18n_helpers(apiclient: TestClient):
    resp = apiclient.get("/fr/dummy-messages")
    assert resp.json() == {
        "dgettext": "addresse email invalide",
        "dngettext_0": "0 entrée dans addresse email",
        "dngettext_1": "1 entrée dans addresse email",
        "dngettext_2": "2 entrées dans addresse email",
        "dnpgettext_0": "0 balls in addresse email",
        "dnpgettext_1": "1 ball in addresse email",
        "dnpgettext_2": "2 balls in addresse email",
        "dpgettext_1": "addresse email (*)",
        "dpgettext_2": "addresse email est requis",
        "gettext": "Le renard marron rapide saute par dessus chient flemmard",
        "ngettext_0": "Le renard marron rapide saute par dessus le chient flemmard",
        "ngettext_1": "Le renard marron rapide saute par dessus le chient flemmard",
        "ngettext_2": "Les 2 renards marron rapides sautent par dessus "
        "le chient flemmard",
        "pgettext_0": "pêcher",
        "pgettext_1": "poisson",
        "npgettext_0": "0 crayon",
        "npgettext_1": "1 crayon",
        "npgettext_2": "2 crayons",
    }

from typing import Any, Mapping

import pytest
from pydantic import SecretStr

from fastlife.request.form import FormModel
from tests.fastlife_app.models import Account


def test_default():
    account = FormModel[Account].default("p", Account)
    assert account.is_valid is False
    assert account.form_data == {
        "p": {"aliases": [], "groups": [], "interest": set(), "recovery_address": None}
    }
    assert account.errors == {}


@pytest.mark.parametrize(
    "payload,expected_valid,expected_form_data,expected_errors",
    [
        pytest.param(
            {},
            False,
            {  # type: ignore
                "p": {
                    "aliases": [],
                    "groups": [],
                    "interest": set(),
                    "recovery_address": None,
                },
            },
            {
                "p.username": "Field required",
                "p.password": "Field required",
                "p.terms_and_conditions": "Field required",
            },
            id="bad-payload",
        ),
        pytest.param(
            {"p": {"username": "Bob"}},
            False,
            {  # type: ignore
                "p": {
                    "username": "Bob",
                    "aliases": [],
                    "groups": [],
                    "interest": set(),
                    "recovery_address": None,
                }
            },
            {
                "p.password": "Field required",
                "p.terms_and_conditions": "Field required",
            },
            id="missing-password-and-contracts",
        ),
        pytest.param(
            {
                "p": {
                    "username": "Bob",
                    "password": "secret123",
                    "terms_and_conditions": "true",
                }
            },
            True,
            {  # type: ignore
                "p": {
                    "username": "Bob",
                    "password": SecretStr("secret123"),
                    "groups": [],
                    "aliases": [],
                    "interest": set(),
                    "recovery_address": None,
                    "terms_and_conditions": True,
                }
            },
            {},
            id="lgtm",
        ),
        pytest.param(
            {
                "p": {
                    "username": "Bob",
                    "password": "secret123",
                    "recovery_address": {
                        "type": "email",
                        "address": "bob@aliceandbob.fr",
                    },
                    "terms_and_conditions": "true",
                }
            },
            True,
            {  # type: ignore
                "p": {
                    "username": "Bob",
                    "password": SecretStr("secret123"),
                    "groups": [],
                    "aliases": [],
                    "interest": set(),
                    "recovery_address": {
                        "type": "email",
                        "address": "bob@aliceandbob.fr",
                    },
                    "terms_and_conditions": True,
                }
            },
            {},
            id="lgtm+recovery",
        ),
    ],
)
def test_from_payload(
    payload: Mapping[str, Any],
    expected_valid: bool,
    expected_form_data: Mapping[str, Any],
    expected_errors: Mapping[str, str],
):
    account = FormModel[Account].from_payload("p", Account, payload)
    assert account.is_valid is expected_valid
    assert account.form_data == expected_form_data
    assert account.errors == expected_errors

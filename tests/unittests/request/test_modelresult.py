from typing import Any, Mapping

import pytest
from pydantic import SecretStr

from fastlife.request.model_result import ModelResult
from tests.fastlife_app.models import Account


def test_default():
    account = ModelResult[Account].default("p", Account)
    assert account.is_valid is False
    assert account.form_data == {
        "p": {"groups": [], "interest": set(), "recovery_address": None}
    }
    assert account.errors == {}


@pytest.mark.parametrize(
    "payload,expected_valid,expected_form_data,expected_errors",
    [
        pytest.param(
            {},
            False,
            {"p": {"groups": [], "interest": set(), "recovery_address": None}},  # type: ignore
            {"p.password": "Field required", "p.username": "Field required"},
        ),
        pytest.param(
            {"p": {"username": "Bob"}},
            False,
            {  # type: ignore
                "p": {
                    "username": "Bob",
                    "groups": [],
                    "interest": set(),
                    "recovery_address": None,
                }
            },
            {"p.password": "Field required"},
        ),
        pytest.param(
            {"p": {"username": "Bob", "password": "secret123"}},
            True,
            {  # type: ignore
                "p": {
                    "username": "Bob",
                    "password": SecretStr("secret123"),
                    "groups": [],
                    "interest": set(),
                    "recovery_address": None,
                }
            },
            {},
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
                }
            },
            True,
            {  # type: ignore
                "p": {
                    "username": "Bob",
                    "password": SecretStr("secret123"),
                    "groups": [],
                    "interest": set(),
                    "recovery_address": {
                        "type": "email",
                        "address": "bob@aliceandbob.fr",
                    },
                }
            },
            {},
        ),
    ],
)
def test_from_payload(
    payload: Mapping[str, Any],
    expected_valid: bool,
    expected_form_data: Mapping[str, Any],
    expected_errors: Mapping[str, str],
):
    account = ModelResult[Account].from_payload("p", Account, payload)
    assert account.is_valid is expected_valid
    assert account.form_data == expected_form_data
    assert account.errors == expected_errors

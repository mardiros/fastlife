from collections.abc import Mapping
from typing import Any

import pytest
from pydantic import SecretStr

from fastlife.domain.model.form import FormModel
from tests.fastlife_app.models import Account
from tests.fastlife_app.views.app.forms.model import Form as ModelForm
from tests.fastlife_app.views.app.forms.model import Person
from tests.fastlife_app.views.app.forms.unionfield import Form as UnionForm

MyModelForm = FormModel[ModelForm]
AccountForm = FormModel[Account]


def test_default():
    account = AccountForm.default("p", Account)
    assert account.is_valid is False
    assert account.form_data == {
        "p": {"aliases": [], "groups": [], "interest": set(), "recovery_address": None}
    }
    assert account.fatal_error == ""
    assert account.errors == {}


def test_fatal_error():
    account = AccountForm.default("p", Account)
    account.set_fatal_error("Internal Server Error")
    assert account.is_valid is False
    assert account.fatal_error == "Internal Server Error"


def test_field_error():
    editform = MyModelForm(
        "x",
        ModelForm.model_construct(),
        errors={"firstname": "missing"},
        is_valid=False,
    )
    p = ModelForm(professor=Person(firstname="Haruto", lastname="Watanabe", age=80))
    editform.edit(p)
    assert editform.model.model_dump() == {
        "professor": {"firstname": "Haruto", "lastname": "Watanabe", "age": 80}
    }
    assert editform.is_valid, (
        "A pydandict model passed in the edit form is always considered valid"
    )


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
    account = AccountForm.from_payload("p", Account, payload)
    assert account.is_valid is expected_valid
    assert account.form_data == expected_form_data
    assert account.errors == expected_errors


@pytest.mark.parametrize(
    "payload,expected_is_valid,expected_form_data,expected_errors",
    [
        pytest.param(
            {},
            False,
            {"x": {}},
            {"x.pet": "Field required"},
            id="default",
        ),
        pytest.param(
            {"x": {"pet": {"type": "cat"}}},
            False,
            {"x": {"pet": {"type": "cat"}}},
            {
                "x.pet.nick": "Field required",
            },
            id="missing field",
        ),
        pytest.param(
            {"x": {"pet": {"type": "cat", "nick": "whisker"}}},
            True,
            {"x": {"pet": {"nick": "whisker", "type": "cat"}}},
            {},
            id="valid",
        ),
    ],
)
def test_from_payload_union(
    payload: dict[str, str],
    expected_is_valid: bool,
    expected_form_data: dict[str, Any],
    expected_errors: dict[str, str],
):
    result = FormModel[UnionForm].from_payload("x", UnionForm, payload)
    assert result.is_valid is expected_is_valid
    assert result.form_data == expected_form_data
    assert result.errors == expected_errors

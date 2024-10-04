from typing import Any

import pytest

from fastlife.request.form import FormModel
from tests.fastlife_app.views.app.forms.model import Form as ModelForm
from tests.fastlife_app.views.app.forms.model import Person
from tests.fastlife_app.views.app.forms.unionfield import Form as UnionForm

MyForm = FormModel[ModelForm]


def test_default():
    default = MyForm.default("x", ModelForm)
    assert default.prefix == "x"
    assert default.model.model_dump() == {}
    assert default.errors == {}, "a default model does not display errors in the form"
    assert not default.is_valid, "the default model is not set as valid"


def test_edit():
    editform = MyForm(
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
    assert (
        editform.is_valid
    ), "A pydandict model passed in the edit form is always considered valid"


def test_form_data():
    editform = MyForm("pfx", ModelForm.model_construct(), errors={})
    p = ModelForm(professor=Person(firstname="Haruto", lastname="Watanabe", age=80))
    editform.edit(p)
    assert editform.form_data == {
        "pfx": {"professor": {"age": 80, "firstname": "Haruto", "lastname": "Watanabe"}}
    }


@pytest.mark.parametrize(
    "payload,expected_is_valid,expected_form_data,expected_errors",
    [
        pytest.param(
            {}, False, {"x": {}}, {"x.professor": "Field required"}, id="default"
        ),
        pytest.param(
            {"x": {"professor": {"age": "80"}}},
            False,
            {"x": {"professor": {"age": "80"}}},
            {
                "x.professor.firstname": "Field required",
                "x.professor.lastname": "Field required",
            },
            id="missing netsted fields",
        ),
        pytest.param(
            {"x": {"professor": {"age": "80", "firstname": "X", "lastname": "Y"}}},
            True,
            {"x": {"professor": {"firstname": "X", "lastname": "Y", "age": 80}}},
            {},
            id="valid",
        ),
    ],
)
def test_from_payload_model(
    payload: dict[str, str],
    expected_is_valid: bool,
    expected_form_data: dict[str, Any],
    expected_errors: dict[str, str],
):
    result = MyForm.from_payload("x", ModelForm, payload)
    assert result.is_valid is expected_is_valid
    assert result.form_data == expected_form_data
    assert result.errors == expected_errors


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
                "x.pet.nick": "Field required, Field required",
                "x.pet.type": "Input should be 'dog'",  # FIXME
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

import pytest

from fastlife.testing import WebTestClient


@pytest.mark.parametrize("typ", ["str", "int", "float"])
def test_show_widget_builtins_str(typ: str, client: WebTestClient):
    resp = client.get(f"/_fl/pydantic-form/widgets/builtins:{typ}?name=nick&token=xxx")
    input = resp.by_label_text("nick")
    assert input is not None
    assert input.attrs["name"] == "nick"
    assert input.attrs["value"] == ""


@pytest.mark.parametrize("typ", ["str", "int", "float"])
def test_show_widget_unions(typ: str, client: WebTestClient):
    resp = client.get(
        "/_fl/pydantic-form/widgets/tests.fastlife_app.models:PhoneNumber|"
        "tests.fastlife_app.models:Email?name=pet&token=xxx"
    )
    assert resp.by_text("PhoneNumber", node_name="button") is not None
    assert resp.by_text("Email", node_name="button") is not None


def test_show_widget_base_model(client: WebTestClient):
    resp = client.get(
        "/_fl/pydantic-form/widgets/tests.fastlife_app.models:PhoneNumber?name=phone&token=xxx"
    )

    input = resp.by_label_text("number")
    assert input is not None
    assert input.attrs["name"] == "phone.number"
    assert input.attrs["value"] == ""

    select = resp.by_label_text("type")  # fixme, should be hidden
    assert select is not None
    assert select.name == "select"
    assert select.attrs["name"] == "phone.type"
    children = [
        (
            str(opt.attrs["value"]),  # type: ignore
            opt.text,
        )
        for opt in select.find_all("option")
    ]
    assert children == [
        ("phonenumber", "phonenumber"),
    ]

import pytest

from fastlife.testing import WebTestClient


@pytest.mark.parametrize("typ", ["str", "int", "float"])
def test_show_widget_builtins_str(typ: str, client: WebTestClient):
    resp = client.get(f"/_fl/pydantic-form/widgets/builtins:{typ}?name=nick&token=xxx")
    input = resp.by_label_text("nick")
    assert input is not None
    assert input.attrs["name"] == "nick"
    assert input.attrs["value"] == ""


def test_show_widget_base_model(client: WebTestClient):
    resp = client.get(
        "/_fl/pydantic-form/widgets/tests.fastlife_app.models:Dog?name=pet&token=xxx"
    )

    input = resp.by_label_text("nick")
    assert input is not None
    assert input.attrs["name"] == "pet.nick"
    assert input.attrs["value"] == ""

    select = resp.by_label_text("breed")
    assert select is not None
    assert select.name == "select"
    assert select.attrs["name"] == "pet.breed"
    children = [
        (
            str(opt.attrs["value"]),  # type: ignore
            opt.text,
        )
        for opt in select.find_all("option")
    ]
    assert children == [
        ("Labrador", "Labrador"),
        ("Golden Retriever", "Golden Retriever"),
        ("Bulldog", "Bulldog"),
    ]

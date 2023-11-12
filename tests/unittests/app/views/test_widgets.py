from fastlife.testing import WebTestClient


def test_show_widget(client: WebTestClient):
    resp = client.get(
        "/_fl/pydantic-form/widgets/tests.fastlife_app.models:Dog?name=pet"
    )

    input = resp.by_label_text("nick")
    assert input is not None
    assert input.attrs["name"] == "pet.nick"
    assert input.attrs["value"] == ""

    input = resp.by_label_text("breed")
    assert input is not None
    assert input.attrs["name"] == "pet.breed"
    assert input.attrs["value"] == ""

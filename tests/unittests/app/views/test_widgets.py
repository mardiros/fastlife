from fastlife.testing import WebTestClient


def test_show_widget(client: WebTestClient):
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

from enum import Enum, IntEnum
from typing import Annotated, Any, Callable, Literal, Sequence, Set

import bs4
from pydantic import BaseModel, EmailStr, Field, SecretStr

from fastlife.request.model_result import ModelResult
from fastlife.templating.renderer.jinjax import JinjaxRenderer
from fastlife.templating.renderer.widgets.base import Widget


class CustomWidget(Widget[Any]):
    def get_template(self) -> str:
        return "CustomWidget"


class Flavor(Enum):
    vanilla = "Vanilla"
    chocolate = "Chocolate"


class Score(IntEnum):
    un = 1
    deux = 2
    trois = 3


class Foo(BaseModel):
    bar: str = Field()
    # private: str = Field(exclude=True)


class Bar(BaseModel):
    foo: str = Field()


class DummyModel(BaseModel):
    name: str = Field()
    description: Annotated[str, CustomWidget] = Field(min_length=2)
    private: str = Field(exclude=True)
    type: Literal["foo", "bar"] = Field()
    flavor: Flavor = Field()
    score: Score = Field()
    passphrase: SecretStr = Field()
    email: EmailStr = Field()
    vegan: bool = Field()
    tags: list[str] = Field()
    foo: Foo = Field()
    foobar: Foo | Bar = Field()


class Tempo(BaseModel):
    id: int = Field()
    name: str = Field()


class CustomSelect(Widget[Any]):
    def get_template(self) -> str:
        return "CustomSelect"


class Banger(BaseModel):
    name: str = Field()
    tempo: Annotated[Sequence[Tempo], CustomSelect] = Field()


class MultiSet(BaseModel):
    flavors: Set[Flavor] = Field(default_factory=set)
    foobarz: Set[Literal["foo", "bar", "baz"]] = Field(default_factory=set)


def test_render_template(
    renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    result = renderer.render_template(
        "DummyForm",
        model=ModelResult[DummyModel].default("payload", DummyModel),
        token="tkt",
    )
    html = soup(result)

    assert html.find(
        "input",
        attrs={"id": "payload-name-tkt", "name": "payload.name", "type": "text"},
    )
    assert (
        html.find(
            "input",
            attrs={
                "id": "payload-private-tkt",
                "name": "payload.private",
                "type": "text",
            },
        )
        is None
    )
    assert html.find(
        "input",
        attrs={
            "id": "payload-passphrase-tkt",
            "name": "payload.passphrase",
            "type": "password",
        },
    )
    assert html.find(
        "input",
        attrs={"id": "payload-email-tkt", "name": "payload.email", "type": "email"},
    )
    assert html.find(
        "div", attrs={"id": "payload-description-tkt", "contenteditable": True}
    )
    assert html.find("select", attrs={"id": "payload-type-tkt"})

    flavors = html.find("select", attrs={"id": "payload-flavor-tkt"})
    assert isinstance(flavors, bs4.Tag)
    vanilla = flavors.find("option", attrs={"value": "vanilla"})
    assert vanilla
    assert vanilla.text.strip() == "Vanilla"
    assert flavors.find("option", attrs={"value": "chocolate"})

    scores = html.find("select", attrs={"id": "payload-score-tkt"})
    assert isinstance(scores, bs4.Tag)
    score_option = scores.find("option", attrs={"value": "deux"})
    assert score_option
    assert score_option.text.strip() == "2"

    assert html.find(
        "input",
        attrs={"id": "payload-vegan-tkt", "name": "payload.vegan", "type": "checkbox"},
    )
    assert html.find(
        "button",
        attrs={"id": "payload-tags-tkt-add", "name": "action", "type": "button"},
    )

    assert html.find(
        "div",
        attrs={"id": "payload-foo-tkt-container"},
    )
    assert html.find(
        "input",
        attrs={"id": "payload-foo-bar-tkt", "name": "payload.foo.bar"},
    )
    assert (
        html.find(
            "input",
            attrs={"id": "payload-foo-private-tkt"},
        )
        is None
    )

    assert html.find(
        "button",
        attrs={"id": "payload-foobar-Foo-tkt", "name": "action", "type": "button"},
    )

    assert html.find(
        "button",
        attrs={"id": "payload-foobar-Bar-tkt", "name": "action", "type": "button"},
    )


def test_render_template_values(
    renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    result = renderer.render_template(
        "DummyForm",
        model=ModelResult[DummyModel].from_payload(
            "payload",
            DummyModel,
            {
                "payload": {
                    "name": "bernard",
                    "description": "-",
                    "type": "bar",
                    "vegan": True,
                    "tags": ["blue", "green"],
                    "foobar": {"foo": "totally"},
                }
            },
        ),
        token="tkt",
    )

    html = soup(result)
    assert html.find(
        "input",
        attrs={
            "id": "payload-name-tkt",
            "name": "payload.name",
            "type": "text",
            "value": "bernard",
        },
    )

    select = html.find("select", attrs={"id": "payload-type-tkt"})
    assert isinstance(select, bs4.Tag)
    assert select.find(
        "option",
        attrs={"value": "bar", "selected": True},
    )

    div = html.find("div", attrs={"id": "payload-description-tkt"})
    assert isinstance(div, bs4.Tag)
    assert div.text == "-"
    err = html.find("p", attrs={"id": "payload-description-tkt-error"})
    assert isinstance(err, bs4.Tag)
    assert err.text == "String should have at least 2 characters"

    assert html.find(
        "input",
        attrs={
            "id": "payload-vegan-tkt",
            "name": "payload.vegan",
            "type": "checkbox",
            "checked": True,
        },
    )

    assert html.find(
        "input",
        attrs={
            "id": "payload-tags-0-tkt",
            "name": "payload.tags.0",
            "type": "text",
            "value": "blue",
        },
    )

    assert html.find(
        "input",
        attrs={
            "id": "payload-tags-1-tkt",
            "name": "payload.tags.1",
            "type": "text",
            "value": "green",
        },
    )

    assert html.find(
        "input",
        attrs={
            "id": "payload-foobar-foo-tkt",
            "name": "payload.foobar.foo",
            "value": "totally",
            "type": "text",
        },
    )


def test_render_custom_list(
    renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    result = renderer.render_template(
        "DummyForm",
        model=ModelResult[Banger].from_payload(
            "payload",
            Banger,
            {
                "payload": {
                    "name": "asturia",
                    "tempo": 1,
                }
            },
        ),
        token="tkt",
        globals={
            "tempos": [Tempo(id=1, name="allegro"), Tempo(id=2, name="piano")],
        },
    )
    html = soup(result)
    assert html.find("option", attrs={"value": "1", "selected": ""})
    assert html.find("option", attrs={"value": "2"})


def test_render_set(renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]):
    result = renderer.render_template(
        "DummyForm",
        model=ModelResult[MultiSet].default("payload", MultiSet),
        token="tkt",
    )
    html = soup(result)
    assert html.find(
        "input",
        attrs={
            "id": "payload-flavors-vanilla-tkt",
            "type": "checkbox",
            "name": "payload.flavors[]",
            "value": "vanilla",
        },
    )

    assert html.find(
        "input",
        attrs={
            "id": "payload-foobarz-foo-tkt",
            "type": "checkbox",
            "name": "payload.foobarz[]",
            "value": "foo",
        },
    )


def test_render_set_checked(
    renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    result = renderer.render_template(
        "DummyForm",
        model=ModelResult[MultiSet].from_payload(
            "payload",
            MultiSet,
            {"payload": {"flavors": ["vanilla"], "foobarz": ["foo"]}},
        ),
        globals={
            "tempos": [Tempo(id=1, name="allegro"), Tempo(id=2, name="piano")],
        },
        token="tkt",
    )
    html = soup(result)
    assert html.find(
        "input",
        attrs={
            "id": "payload-flavors-vanilla-tkt",
            "name": "payload.flavors[]",
            "value": "vanilla",
            "type": "checkbox",
            "checked": True,
        },
    )

    assert html.find(
        "input",
        attrs={
            "id": "payload-foobarz-foo-tkt",
            "type": "checkbox",
            "name": "payload.foobarz[]",
            "value": "foo",
            "checked": True,
        },
    )

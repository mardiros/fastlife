from enum import Enum, IntEnum
from typing import Annotated, Any, Callable, Literal, Sequence

import bs4
from pydantic import BaseModel, EmailStr, Field, SecretStr

from fastlife.templating.renderer.jinjax import AbstractTemplateRenderer
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
    private: str = Field(exclude=True)


class Bar(BaseModel):
    foo: str = Field()


class DummyModel(BaseModel):
    name: str = Field()
    description: Annotated[str, CustomWidget] = Field()
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


def test_render_template(
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    result = renderer.render_template(
        "DummyForm", model=DummyModel, form_data=None, token="tkt"
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
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    result = renderer.render_template(
        "DummyForm",
        model=DummyModel,
        form_data={
            "payload": {
                "name": "bernard",
                "type": "bar",
                "vegan": True,
                "tags": ["blue", "green"],
                "foobar": {"foo": "totally"},
            }
        },
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
    renderer: AbstractTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    result = renderer.render_template(
        "DummyForm",
        model=Banger,
        form_data={
            "name": "asturia",
            "tempo": 1,
        },
        token="tkt",
        globals={
            "tempos": [Tempo(id=1, name="allegro"), Tempo(id=2, name="piano")],
        },
    )
    html = soup(result)
    assert html.find("option", attrs={"value": "1", "selected": ""})
    assert html.find("option", attrs={"value": "2"})

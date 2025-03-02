from collections.abc import Callable, Sequence
from enum import Enum, IntEnum
from typing import Annotated, Any, Literal

import bs4
from pydantic import BaseModel, EmailStr, Field, SecretStr

from fastlife.adapters.jinjax.renderer import JinjaxRenderer
from fastlife.adapters.jinjax.widgets.base import CustomWidget, Widget
from fastlife.domain.model.form import FormModel
from tests.unittests.templates.test_jinjax_components import JinjaXTemplate


class MyWidget(Widget[str]):
    template = """
    <div id="{{id}}" contenteditable>{{value}}</div>
    {% if error %}
    <p id="{{id}}-error">{{error}}</p>
    {% endif %}
    """


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


class DummyOptional(BaseModel):
    foobar: str | None = Field()


class DummyModel(BaseModel):
    name: str = Field()
    description: Annotated[str, CustomWidget(MyWidget)] = Field(min_length=2)
    private: str = Field(exclude=True)
    type: Literal["foo", "bar"] = Field()
    flavor: Flavor = Field()
    score: Score = Field()
    passphrase: SecretStr = Field()
    newpass: Annotated[SecretStr, "new-password"] = Field()
    email: EmailStr = Field()
    vegan: bool = Field()
    tags: list[str] = Field()
    foo: Foo = Field()
    foobar: Foo | Bar = Field()


class Tempo(BaseModel):
    id: int = Field()
    name: str = Field()


class CustomSelect(Widget[Any]):
    template = """
    <Select :name="name" :id="id" multiple>
      {% for tempo in tempos %}
      <Option :value="tempo.id" :selected="value==tempo.id">
        {{tempo.name}}
      </Option>
      {% endfor %}
    </Select>
    """


class Banger(BaseModel):
    name: str = Field()
    tempo: Annotated[Sequence[Tempo], CustomWidget(CustomSelect)] = Field()


class MultiSet(BaseModel):
    flavors: set[Flavor] = Field(default_factory=set)
    foobarz: set[Literal["foo", "bar", "baz"]] = Field(default_factory=set)


class DummyForm(JinjaXTemplate):
    template = """
    <Form>
      {{ pydantic_form(model=model, token=token) }}
      <Button>Submit</Button>
    </Form>
    """
    model: FormModel[DummyModel | Banger | MultiSet | DummyOptional]
    token: str


def test_render_template(
    renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=FormModel[DummyModel | Banger | MultiSet | DummyOptional].default(
            "payload", DummyModel
        ),
        token="tkt",
    )
    result = renderer.render_template(form)
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
            "autocomplete": "current-password",
        },
    )
    assert html.find(
        "input",
        attrs={
            "id": "payload-newpass-tkt",
            "name": "payload.newpass",
            "type": "password",
            "autocomplete": "new-password",
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


def test_render_fatal_error(renderer: JinjaxRenderer):
    form = DummyForm(
        model=FormModel[DummyModel | Banger | MultiSet | DummyOptional].default(
            "payload", DummyModel
        ),
        token="tkt",
    )
    result = renderer.render_template(form)
    assert ' role="alert"' not in result
    assert '<span class="sm:inline text-xl">' not in result
    form.model.set_fatal_error("Internal Server Error")
    result = renderer.render_template(form)
    assert ' role="alert"' in result
    assert '<span class="sm:inline text-xl">Internal Server Error</span>' in result


def test_render_template_values(
    renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=FormModel[DummyModel | Banger | MultiSet | DummyOptional].from_payload(
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
    result = renderer.render_template(form)

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
    form = DummyForm(
        model=FormModel[DummyModel | Banger | MultiSet | DummyOptional].from_payload(
            "payload",
            Banger,
            {
                "payload": {
                    "name": "asturia",
                    "tempo": [1],
                }
            },
        ),
        token="tkt",
    )
    renderer.globals.update(
        {
            "tempos": [Tempo(id=1, name="allegro"), Tempo(id=2, name="piano")],
        }
    )

    result = renderer.render_template(form)

    html = soup(result)
    assert html.find("option", attrs={"value": "1", "selected": ""})
    assert html.find("option", attrs={"value": "2"})


def test_render_set(renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]):
    form = DummyForm(
        model=FormModel[DummyModel | Banger | MultiSet | DummyOptional].default(
            "payload", MultiSet
        ),
        token="tkt",
    )

    result = renderer.render_template(form)
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
    form = DummyForm(
        model=FormModel[DummyModel | Banger | MultiSet | DummyOptional].from_payload(
            "payload",
            MultiSet,
            {"payload": {"flavors": ["vanilla"], "foobarz": ["foo"]}},
        ),
        token="tkt",
    )
    renderer.globals.update(
        {
            "tempos": [Tempo(id=1, name="allegro"), Tempo(id=2, name="piano")],
        }
    )

    result = renderer.render_template(form)

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


def test_render_optional(
    renderer: JinjaxRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=FormModel[DummyModel | Banger | MultiSet | DummyOptional].default(
            "payload", DummyOptional
        ),
        token="tkt",
    )

    result = renderer.render_template(form)
    html = soup(result)
    assert html.find(
        "input",
        attrs={
            "id": "payload-foobar-tkt",
            "type": "text",
            "name": "payload.foobar",
            "value": "",
        },
    )

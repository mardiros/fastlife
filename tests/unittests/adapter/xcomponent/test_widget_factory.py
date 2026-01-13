from collections.abc import Callable, Sequence
from datetime import date, datetime
from decimal import Decimal
from enum import Enum, IntEnum
from typing import Annotated, Any, Literal, NewType
from uuid import UUID

import bs4
import pytest
from lastuuid.dummies import uuidgen
from pydantic import BaseModel, EmailStr, Field, IPvAnyAddress, SecretStr
from pydantic.fields import FieldInfo

from fastlife.adapters.xcomponent.pydantic_form.widget_factory.factory import (
    WidgetFactory,
)
from fastlife.adapters.xcomponent.pydantic_form.widget_factory.union_builder import (
    get_child_widget,
    get_title,
    get_title_from_discriminator,
    get_type_from_discriminator,
)
from fastlife.adapters.xcomponent.pydantic_form.widgets.base import CustomWidget, Widget
from fastlife.adapters.xcomponent.renderer import XTemplateRenderer
from fastlife.domain.model.form import FormModel
from fastlife.domain.model.template import XTemplate
from tests.fastlife_app.views.app.i18n.dummy_messages import gettext

UserId = NewType("UserId", UUID)


class User(BaseModel):
    user_id: UserId = Field(title="User Id")


class MyWidget(Widget[str]):
    template = """
    <>
        <h6>{custom_title}</title>
        <div id={id} contenteditable>{value}</div>
        {
            if error {
                <p id={id + "-error"}>{error}</p>
            }
        }
    </>
    """
    custom_title: str


class Flavor(Enum):
    VANILLA = "Vanilla"
    CHOCOLATE = "Chocolate"


class Score(IntEnum):
    un = 1
    deux = 2
    trois = 3


class Foo(BaseModel):
    type: Literal["foo"] = "foo"
    bar: str = Field()
    # private: str = Field(exclude=True)


class Bar(BaseModel):
    type: Literal["bar"] = "bar"
    foo: str = Field()


class DummyOptional(BaseModel):
    foobar: str | None = Field()


class DummyDate(BaseModel):
    started_on: date = Field()
    ended_on: date | None = Field()


class DummyDateTime(BaseModel):
    started_at: datetime = Field()
    ended_at: datetime | None = Field()


class DummyCustomized(BaseModel):
    dummy: Annotated[str, CustomWidget(MyWidget, custom_title="my dummy")] = Field(
        min_length=2
    )


class DummyIntEnum(BaseModel):
    dummy: Score = Field(default=Score.deux)


class DummyModel(BaseModel):
    identifier: UUID = Field(default=uuidgen(1))
    category: Literal["dummy"] = Field()
    name: str = Field()
    description: Annotated[str, CustomWidget(MyWidget, custom_title="title")] = Field(
        min_length=2
    )
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
    foobar: Foo | Annotated[Bar, "the bar"] = Field(discriminator="type")
    address: IPvAnyAddress = Field()


class Tempo(BaseModel):
    id: int = Field()
    name: str = Field()


class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"


class Price(BaseModel):
    amount: Decimal
    currency: Currency


class CustomSelect(Widget[Any]):
    template = """
    <Select name={name} id={id} multiple>
      {
        for tempo in globals.tempos {
            <Option value={tempo.id} selected={ value==tempo.id }>
                {tempo.name}
            </Option>
        }
    }
    </Select>
    """


class Banger(BaseModel):
    name: str = Field()
    tempo: Annotated[Sequence[Tempo], CustomWidget(CustomSelect)] = Field()


class MultiSet(BaseModel):
    flavors: set[Flavor] = Field(default_factory=set)
    foobarz: set[Literal["foo", "bar", "baz"]] = Field(default_factory=set)


DummyFormModel = FormModel[
    DummyModel
    | Banger
    | MultiSet
    | DummyOptional
    | DummyCustomized
    | DummyIntEnum
    | DummyDate
    | DummyDateTime
]


class DummyForm(XTemplate):
    template = """
    <Form>
      { globals.pydantic_form(model=model, token=token) }
      <Button>Submit</Button>
    </Form>
    """
    model: DummyFormModel
    token: str


class PriceForm(XTemplate):
    template = """
    <Form>
      { globals.pydantic_form(model=model, token=token) }
      <Button>Submit</Button>
    </Form>
    """
    model: FormModel[Price]
    token: str


class UserForm(XTemplate):
    template = """
    <Form>
      { globals.pydantic_form(model=model, token=token) }
      <Button>Submit</Button>
    </Form>
    """
    model: FormModel[User]
    token: str


@pytest.fixture
def factory(renderer: XTemplateRenderer):
    return WidgetFactory(renderer, "x")


@pytest.mark.parametrize(
    "typ,expected",
    [
        (Foo, "Foo"),
        (Annotated[Foo, "the foo"], "the foo"),
        (Annotated[Foo, gettext("the foo")], "the foo"),
    ],
)
def test_get_title(typ: type[Any], expected: str):
    assert get_title(typ) == expected


@pytest.mark.parametrize(
    "discriminant,field,expected",
    [
        pytest.param("foo", DummyModel.model_fields["foobar"], "Foo", id="type"),
        pytest.param(
            "bar", DummyModel.model_fields["foobar"], "the bar", id="annotated type"
        ),
        pytest.param("baz", DummyModel.model_fields["foobar"], "baz", id="unknown"),
    ],
)
def test_get_title_from_discriminator(
    discriminant: str, field: FieldInfo, expected: str
):
    assert get_title_from_discriminator(discriminant, field) == expected


@pytest.mark.parametrize(
    "field,value,expected",
    [
        pytest.param(None, None, None, id="none"),
        pytest.param(
            DummyModel.model_fields["foobar"],
            {"type": "foo", "bar": "foobar"},
            {
                "name": "dummy_name",
                "id": "dummy-name-x",
                "value": [
                    {
                        "name": "dummy_name.type",
                        "id": "dummy-name-type-x",
                        "value": "foo",
                        "title": "type",
                        "token": "x",
                    },
                    {
                        "name": "dummy_name.bar",
                        "id": "dummy-name-bar-x",
                        "value": "foobar",
                        "title": "bar",
                        "token": "x",
                    },
                ],
                "title": "Foo",
                "token": "x",
                "nested": True,
            },
            id="value",
        ),
        pytest.param(
            DummyModel.model_fields["foobar"],
            {"type": "foo"},
            {
                "id": "dummy-name-x",
                "name": "dummy_name",
                "nested": True,
                "title": "Foo",
                "token": "x",
                "value": [
                    {
                        "id": "dummy-name-type-x",
                        "name": "dummy_name.type",
                        "title": "type",
                        "token": "x",
                        "value": "foo",
                    },
                    {
                        "id": "dummy-name-bar-x",
                        "name": "dummy_name.bar",
                        "title": "bar",
                        "token": "x",
                        "value": "",
                    },
                ],
            },
            id="invalid",
        ),
    ],
)
def test_get_child_widget(
    factory: WidgetFactory,
    field: FieldInfo | None,
    value: Any,
    expected: Widget[Any] | None,
):
    widget = get_child_widget(
        field,
        value,
        factory,
        "dummy_name",
        {},
    )
    dump = None
    if widget != None:
        dump = widget.model_dump(
            exclude_none=True, exclude_defaults=True, exclude_unset=True
        )
    assert dump == expected


@pytest.mark.parametrize(
    "discriminant,field,expected",
    [
        pytest.param("foo", DummyModel.model_fields["foobar"], Foo, id="type"),
        pytest.param(
            "bar", DummyModel.model_fields["foobar"], Bar, id="annotated type"
        ),
        pytest.param("baz", DummyModel.model_fields["foobar"], None, id="unknown"),
    ],
)
def test_get_type_from_discriminator(
    discriminant: str, field: FieldInfo, expected: Any
):
    assert get_type_from_discriminator(discriminant, field) == expected


def test_render_template(
    renderer: XTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=DummyFormModel.default("payload", DummyModel),
        token="tkt",
    )
    result = renderer.render_template(form)
    html = soup(result)
    assert html.find(
        "input",
        attrs={
            "id": "payload-identifier-tkt",
            "name": "payload.identifier",
            "type": "hidden",
            "value": str(uuidgen(1)),
        },
    )

    assert html.find(
        "input",
        attrs={
            "id": "payload-name-tkt",
            "name": "payload.name",
            "type": "text",
            "value": "",
        },
    )
    assert html.find(
        "input",
        attrs={
            "id": "payload-address-tkt",
            "name": "payload.address",
            "type": "text",
            "value": "",
        },
    )
    assert (
        html.find(
            "input",
            attrs={
                "id": "payload-private-tkt",
                "name": "payload.private",
                "type": "text",
                "value": "",
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
        attrs={
            "id": "payload-email-tkt",
            "name": "payload.email",
            "type": "email",
            "autocomplete": "email",
        },
    )
    assert html.find(
        "div", attrs={"id": "payload-description-tkt", "contenteditable": True}
    )
    assert html.find("select", attrs={"id": "payload-type-tkt"})

    flavors = html.find("select", attrs={"id": "payload-flavor-tkt"})
    assert isinstance(flavors, bs4.Tag)
    vanilla = flavors.find("option", attrs={"value": "Vanilla"})
    assert vanilla
    assert vanilla.text.strip() == "Vanilla"
    assert flavors.find("option", attrs={"value": "Chocolate"})

    scores = html.find("select", attrs={"id": "payload-score-tkt"})
    assert isinstance(scores, bs4.Tag)
    score_option = scores.find("option", attrs={"value": "2"})
    assert score_option
    assert score_option.text.strip() == "2"

    assert html.find(
        "input",
        attrs={
            "id": "payload-category-tkt",
            "name": "payload.category",
            "type": "hidden",
            "value": "dummy",
        },
    )
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


def test_render_fatal_error(renderer: XTemplateRenderer):
    form = DummyForm(
        model=DummyFormModel.default("payload", DummyModel),
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
    renderer: XTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=DummyFormModel.from_payload(
            "payload",
            DummyModel,
            {
                "payload": {
                    "name": "bernard",
                    "description": "-",
                    "type": "bar",
                    "vegan": True,
                    "tags": ["blue", "green"],
                    "foobar": {"type": "bar", "foo": "totally"},
                    "address": "192.168.3.4",
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

    assert html.find(
        "input",
        attrs={
            "id": "payload-address-tkt",
            "name": "payload.address",
            "type": "text",
            "value": "192.168.3.4",
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
    renderer: XTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=DummyFormModel.from_payload(
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


def test_render_set(
    renderer: XTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=DummyFormModel.default("payload", MultiSet),
        token="tkt",
    )

    result = renderer.render_template(form)
    html = soup(result)

    assert html.find(
        "input",
        attrs={
            "id": "payload-flavors-Vanilla-tkt",
            "type": "checkbox",
            "name": "payload.flavors[]",
            "value": "Vanilla",
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
    renderer: XTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=DummyFormModel.from_payload(
            "payload",
            MultiSet,
            {"payload": {"flavors": ["Vanilla"], "foobarz": ["foo"]}},
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
            "id": "payload-flavors-Vanilla-tkt",
            "name": "payload.flavors[]",
            "value": "Vanilla",
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
    renderer: XTemplateRenderer, soup: Callable[[str], bs4.BeautifulSoup]
):
    form = DummyForm(
        model=DummyFormModel.default("payload", DummyOptional),
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


@pytest.mark.parametrize(
    "amount,currency,expected",
    [
        pytest.param(
            "-",
            "EUR",
            {
                "id": "x-currency-tkt-EUR",
                "value": "EUR",
                "selected": "",
            },
            id="valid-currency-form-invalid",
        ),
        pytest.param(
            "-",
            "TWD",
            {
                "id": "x-currency-tkt-EUR",
                "value": "EUR",
            },
            id="valid-currency-form-invalid",
        ),
        pytest.param(
            "42.10",
            "EUR",
            {
                "id": "x-currency-tkt-EUR",
                "value": "EUR",
                "selected": "",
            },
            id="valid-currency-form-valid",
        ),
    ],
)
def test_render_invalid_payload(
    renderer: XTemplateRenderer,
    amount: str,
    currency: str,
    expected: dict[str, str],
    soup: Callable[[str], bs4.BeautifulSoup],
):
    invalid_price = Price.model_construct(
        amount=amount,
        currency=currency,
    )
    model = FormModel[Price].default("x", Price)
    model.edit(invalid_price)
    form = PriceForm(
        model=model,
        token="tkt",
    )

    result = renderer.render_template(form)
    html = soup(result)
    assert html.find("option", attrs=expected)


def test_render_new_type(
    renderer: XTemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
):
    new_user = User.model_construct()

    model = FormModel[User].default("x", User)
    model.edit(new_user)
    form = UserForm(
        model=model,
        token="tkt",
    )

    result = renderer.render_template(form)
    html = soup(result)
    assert html.find("input", attrs={"name": "x.user_id", "type": "hidden"})


def test_render_parametrized_custom_widget(
    renderer: XTemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
):
    cust = DummyCustomized.model_construct()

    model = FormModel[DummyCustomized].default("x", DummyCustomized)
    model.edit(cust)
    form = DummyForm(
        model=model,  # type: ignore
        token="tkt",
    )

    result = renderer.render_template(form)
    html = soup(result)
    h6 = html.find("h6")
    assert h6 and h6.text == "my dummy"


def test_render_intenum(
    renderer: XTemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
):
    intenum = DummyIntEnum.model_construct()

    model = FormModel[DummyIntEnum].default("x", DummyIntEnum)
    model.edit(intenum)
    form = DummyForm(
        model=model,  # type: ignore
        token="tkt",
    )

    result = renderer.render_template(form)
    html = soup(result)
    select = html.find("select")
    assert select and select.text == "123"


def test_render_date(
    renderer: XTemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
):
    fieldset = DummyDate.model_construct()

    model = FormModel[DummyDate].default("x", DummyDate)
    model.edit(fieldset)
    form = DummyForm(
        model=model,  # type: ignore
        token="tkt",
    )

    result = renderer.render_template(form)
    html = soup(result)
    input = html.find("input", attrs={"type": "date", "name": "x.started_on"})
    assert input is not None, result
    input = html.find("input", attrs={"type": "date", "name": "x.ended_on"})
    assert input is not None, result


def test_render_datetime(
    renderer: XTemplateRenderer,
    soup: Callable[[str], bs4.BeautifulSoup],
):
    fieldset = DummyDateTime.model_construct()

    model = FormModel[DummyDateTime].default("x", DummyDateTime)
    model.edit(fieldset)
    form = DummyForm(
        model=model,  # type: ignore
        token="tkt",
    )

    result = renderer.render_template(form)
    html = soup(result)
    input = html.find("input", attrs={"type": "datetime-local", "name": "x.started_at"})
    assert input is not None, result
    input = html.find("input", attrs={"type": "datetime-local", "name": "x.ended_at"})
    assert input is not None, result

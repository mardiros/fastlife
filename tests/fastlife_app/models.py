from collections.abc import Sequence
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, SecretStr, field_validator

from fastlife.adapters.jinjax.widgets.base import Widget


class Person(BaseModel):
    nick: str


class GroupsChoice(Widget[Any]):
    def get_template(self) -> str:
        return "GroupsChoice.jinja"


class Permission(BaseModel):
    name: str = Field(title="Permission")


def nextid():
    id = 1
    while True:
        yield id
        id += 1


_groupid = nextid()


class Group(BaseModel):
    id: int = Field(default_factory=lambda: next(_groupid))
    name: str = Field(title="Group name")
    permissions: list[Permission] = Field(title="Permissions", default_factory=list)

    @field_validator("permissions")
    def validate_permissions(cls, value: Any) -> Any:
        if value:
            return [val for val in value if val is not None]
        return value


class PhoneNumber(BaseModel):
    type: Literal["phonenumber"] = Field(default="phonenumber", title="Phone")
    number: str = Field(min_length=4)


class Email(BaseModel):
    type: Literal["email"] = Field(default="email", title="Email")
    address: str = Field(min_length=5)


Interest = Literal["music", "cinema", "sport"]


class Account(BaseModel):
    username: str = Field(
        title="Username",
        description="Your unique identifier",
        examples=["alice", "bob"],
        min_length=3,
        pattern="^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]$",
    )
    password: SecretStr = Field(
        title="Password",
        description="The painfull secret you should put in your password manager",
    )
    recovery_address: PhoneNumber | Email | None = Field(
        title="Email or Phone",
        description="Email or Phone number used to recover your account, "
        "in case you lost your password",
        default=None,
    )

    groups: Annotated[list[Group], GroupsChoice] = Field(
        title="Group", default_factory=list
    )

    aliases: Sequence[str] = Field(default_factory=list)
    interest: set[Interest] = Field(default_factory=set)

    terms_and_conditions: bool = Field(
        # Add models.py in the content section of tailwind.config.js
        title="I accept <a class='text-primary-600' href='#'>terms and conditions</a>."
    )

    @field_validator("groups")
    @classmethod
    def validate_groups(cls, value: Any) -> Any:
        if value:
            return [val for val in value if val is not None]
        return value

    @field_validator("terms_and_conditions", mode="after")
    @classmethod
    def validate_terms_and_conditions(cls, value: Any) -> Any:
        if value is not True:
            raise ValueError("You must accept term and condition")
        return value

from typing import Annotated, Any, Literal, Set

from pydantic import BaseModel, Field, SecretStr, field_validator

from fastlife.templating.renderer.widgets.base import Widget


class Checklist(Widget[Any]):
    def get_template(self) -> str:
        return "Checklist"


class Permission(BaseModel):
    name: str = Field(title="Permission")


class Group(BaseModel):
    name: str = Field(title="Group name")
    permissions: list[Permission] = Field(title="Permissions", default_factory=list)

    @field_validator("permissions")
    def validate_permissions(cls, value: Any) -> Any:
        if value:
            return [val for val in value if val is not None]
        return value


class PhoneNumber(BaseModel):
    type: Literal["phonenumber"] = Field(default="phonenumber")
    number: str = Field(min_length=4)


class Email(BaseModel):
    type: Literal["email"] = Field(default="email")
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

    groups: Annotated[list[Group], Checklist] = Field(
        title="Group", default_factory=list
    )

    interest: Set[Interest] = Field(default_factory=set)

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

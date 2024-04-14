from typing import Annotated, Any, Literal, Optional

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
    number: str = Field(...)


class Email(BaseModel):
    type: Literal["email"] = Field(default="email")
    address: str = Field(...)


class Account(BaseModel):
    username: str = Field(
        title="Username",
        description="Your unique identifier",
        examples=["alice", "bob"],
    )
    password: Optional[SecretStr] = Field(
        title="Password",
        description="The painfull secret you should put in your password manager",
        default=None,
    )
    recovery_address: Optional[PhoneNumber | Email] = Field(
        title="Email or Phone",
        description="Email or Phone number used to recover your account, "
        "in case you lost your password",
        default=None,
    )

    groups: Annotated[list[Group], Checklist] = Field(
        title="Group", default_factory=list
    )

    @field_validator("groups")
    def validate_groups(cls, value: Any) -> Any:
        if value:
            return [val for val in value if val is not None]
        return value

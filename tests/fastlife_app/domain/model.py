import secrets
from uuid import UUID, uuid1

from pydantic import BaseModel

from tests.fastlife_app.models import Field


class UserAccount(BaseModel):
    user_id: UUID = Field(default_factory=uuid1)
    username: str
    permissions: set[str]


class AuthnToken(BaseModel):
    authntoken_id: UUID = Field(default_factory=uuid1)
    user_id: UUID
    username: str
    permissions: set[str]

    def has_permission(self, permission_name: str) -> bool:
        return permission_name in self.permissions


class TokenInfo(BaseModel):
    token: str = Field(default_factory=secrets.token_urlsafe)
    user_id: UUID
    username: str

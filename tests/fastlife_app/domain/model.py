from pydantic import BaseModel


class AuthenticatedUser(BaseModel):
    user_id: str
    username: str
    permissions: set[str]

    def has_permission(self, permission_name: str) -> bool:
        return permission_name in self.permissions

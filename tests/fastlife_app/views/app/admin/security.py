from uuid import UUID

from starlette.status import HTTP_303_SEE_OTHER

from fastlife import (
    AbstractSecurityPolicy,
    Allowed,
    Anonymous,
    Authenticated,
    AuthenticationState,
    Configurator,
    Denied,
    HasPermission,
    PendingMFA,
    PreAuthenticated,
    Request,
    Response,
    Unauthenticated,
    Unauthorized,
    configure,
    exception_handler,
)
from tests.fastlife_app.config import MyRequest
from tests.fastlife_app.domain.model import UserAccount
from tests.fastlife_app.service.uow import AuthnToken
from tests.fastlife_app.views.api.security import (
    MyRegistry,
)


class RedirectLogin(Unauthorized):
    """Own exception to attach the proper exception handler."""


@exception_handler(RedirectLogin)
def redict_login(request: Request, exception: RedirectLogin):
    return Response(
        "See Other",
        status_code=HTTP_303_SEE_OTHER,
        headers={"Location": str(request.url_for("login"))},
    )


class SecurityPolicy(AbstractSecurityPolicy[MyRegistry, AuthnToken, UserAccount]):
    Unauthorized = RedirectLogin

    def __init__(self, request: MyRequest):
        super().__init__(request)
        self.uow = request.registry.uow

    async def build_authentication_state(
        self,
    ) -> AuthenticationState[UserAccount, AuthnToken]:
        if "authntoken_id" in self.request.session:
            tok = await self.uow.tokens.get_by_id(
                UUID(self.request.session["authntoken_id"])
            )
            assert tok
            return Authenticated(tok)
        elif "user_id" in self.request.session:
            user = await self.uow.users.get_user_by_id(
                UUID(self.request.session["user_id"])
            )
            assert user
            return PendingMFA(
                UserAccount(
                    user_id=user.user_id,
                    username=user.username,
                    permissions={"mfa:validate"},  # we don't wan't all the permissions
                )
            )
        else:
            return Anonymous

    async def has_permission(
        self, permission: str
    ) -> type[HasPermission] | HasPermission:
        """Allow access to everything if signed in."""

        state = await self.get_authentication_state()
        match state:
            case Authenticated(identity):
                if identity.has_permission(permission):
                    return Allowed
            case PendingMFA(_):
                return PreAuthenticated
            case _:
                return Unauthenticated

        return Denied(f"User not granted to perform {permission}")

    async def pre_remember(self, claimed_identity: UserAccount) -> None:
        self.request.session["user_id"] = str(claimed_identity.user_id)

    async def remember(self, identity: AuthnToken) -> None:
        self.request.session["authntoken_id"] = str(identity.authntoken_id)

    async def forget(self) -> None:
        self.request.session.clear()


async def get_authenticated_user(request: MyRequest) -> AuthnToken | None:
    if request.security_policy is None:
        return None
    return await request.security_policy.identity()


@configure
def includeme(config: Configurator):
    config.set_security_policy(SecurityPolicy)
    config.add_renderer_global("authenticated_user", get_authenticated_user)

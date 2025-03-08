"""Security policy permission routine."""

from collections.abc import Callable, Coroutine
from typing import Any

CheckPermissionHook = Callable[..., Coroutine[Any, Any, None]] | Callable[..., None]
CheckPermission = Callable[[str], CheckPermissionHook]


def check_permission(permission_name: str) -> CheckPermissionHook:
    """
    A closure that check that a user as the given permission_name.

    Adding a permission on the route requires that a security policy has been
    added using the method
    {meth}`fastlife.config.configurator.GenericConfigurator.set_security_policy`

    :param permission_name: a permission name set in a view to check access.
    :return: a function that raise http exceptions or any configured exception here.
    """
    # the check_permission is called by the configurator
    # and the request is exposed in the public module creating a circular dependency.
    from fastlife import Request  # a type must be resolved to inject a dependency.

    async def depencency_injection(request: Request) -> None:
        if request.security_policy is None:
            raise RuntimeError(
                f"Request {request.url.path} require a security policy, "
                "explicit fastlife.service.security_policy.InsecurePolicy is required"
            )
        allowed = await request.security_policy.has_permission(permission_name)
        match allowed.kind:
            case "allowed":
                return
            case "denied":
                raise request.security_policy.Forbidden(detail=allowed.reason)
            case "mfa_required":
                raise request.security_policy.MFARequired(detail=allowed.reason)
            case "unauthenticated":
                raise request.security_policy.Unauthorized(detail=allowed.reason)

    return depencency_injection

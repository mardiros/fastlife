from typing import Any, Callable, Coroutine

CheckPermissionHook = Callable[..., Coroutine[Any, Any, None]] | Callable[..., None]
CheckPermission = Callable[[str], CheckPermissionHook]


def check_permission(permission_name: str) -> CheckPermissionHook:
    """
    A closure that check that a user as the given username.

    This method has to be overriden using the setting check_permission
    to implement it.
    """

    def depencency_injection() -> None:
        ...

    return depencency_injection

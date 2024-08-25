"""Security policy."""
from typing import Any, Callable, Coroutine

CheckPermissionHook = Callable[..., Coroutine[Any, Any, None]] | Callable[..., None]
CheckPermission = Callable[[str], CheckPermissionHook]


def check_permission(permission_name: str) -> CheckPermissionHook:
    """
    A closure that check that a user as the given permission_name.

    This method has to be overriden using the setting
    :attr:`fastlife.config.settings.Settings.check_permission` to implement it.

    When the check permission is properly set in the settings., the hook is called
    for every route added with a permission keyword.
    :meth:`fastlife.config.configurator.Configurator.add_route`

    :param permission_name: a permission name set in a view to check access.
    :return: a function that raise http exceptions or any configured exception here.
    """

    def depencency_injection() -> None:
        ...

    return depencency_injection

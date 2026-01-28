"""
Tamahagane registry.

Hooks are attached to a category on import, and then the scanner
will attach a decorated method to the its instanciated configurator.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import tamahagane as th

if TYPE_CHECKING:
    from fastlife.config.configurator import GenericConfigurator


@dataclass
class RegistryHub:
    """Hold a category with its associated registry."""

    fastlife: "GenericConfigurator[Any]"
    """The framework registry."""


TH_CATEGORY = "fastlife"


FastlifeScanner = th.Scanner[RegistryHub]


def th_attach(
    wrapped: "th.scanner.RegisteredFn",
    callback: th.scanner.CallbackHook[RegistryHub],
) -> None:
    """Attach the callback the registry."""
    FastlifeScanner.attach(wrapped, callback, TH_CATEGORY)

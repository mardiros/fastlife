"""
Tamahagane registry.

Hooks are attached to a category on import, and then the scanner
will attach a decorated method to the its instanciated configurator.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastlife.config.configurator import GenericConfigurator


@dataclass
class THRegistry:
    """Hold a category with its associated registry."""

    fastlife: "GenericConfigurator[Any]"
    """The framework registry."""


TH_CATEGORY = "fastlife"

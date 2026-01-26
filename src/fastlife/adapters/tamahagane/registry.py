from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastlife.config.configurator import GenericConfigurator


@dataclass
class THRegistry:
    fastlife: "GenericConfigurator[Any]"


TH_CATEGORY = "fastlife"

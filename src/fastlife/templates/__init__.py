"""
Utilities for rendering HTML templates for page and components as FastAPI dependencies.
"""

from .binding import Template, template
from .inline import InlineTemplate

__all__ = [
    "Template",
    "template",
    "InlineTemplate",
]

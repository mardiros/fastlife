"""Abstract class for builder."""

import abc
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic.fields import FieldInfo

from fastlife.adapters.jinjax.widgets.base import Widget

if TYPE_CHECKING:
    from fastlife.adapters.jinjax.widget_factory.factory import (  # coverage: ignore
        WidgetFactory,
    )

T = TypeVar("T")


class BaseWidgetBuilder(abc.ABC, Generic[T]):
    """Base class for the builder of widget."""

    def __init__(self, factory: "WidgetFactory") -> None:
        self.factory = factory

    @abc.abstractmethod
    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """Return true if the builder accept to build a widget for this type."""

    @abc.abstractmethod
    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: T | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> Widget[T]:
        """Build the widget"""

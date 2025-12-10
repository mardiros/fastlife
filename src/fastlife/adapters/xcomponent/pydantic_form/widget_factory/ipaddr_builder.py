"""Handle boolean values."""

from collections.abc import Mapping
from typing import Any

from pydantic import IPvAnyAddress
from pydantic.fields import FieldInfo

from fastlife.adapters.xcomponent.pydantic_form.widget_factory.base import (
    BaseWidgetBuilder,
)
from fastlife.adapters.xcomponent.pydantic_form.widgets.ip_address import (
    IpAddressWidget,
)


class IpAddrBuilder(BaseWidgetBuilder[IPvAnyAddress]):
    """Builder for boolean."""

    def accept(self, typ: type[Any], origin: type[Any] | None) -> bool:
        """True for boolean."""
        return issubclass(typ, IPvAnyAddress)

    def build(
        self,
        *,
        field_name: str,
        field_type: type[Any],
        field: FieldInfo | None,
        value: IPvAnyAddress | None,
        form_errors: Mapping[str, Any],
        removable: bool,
    ) -> IpAddressWidget:
        """Build the widget."""
        return IpAddressWidget(
            name=field_name,
            removable=removable,
            title=field.title or "" if field else "",
            hint=field.description if field else None,
            aria_label=(
                field.json_schema_extra.get("aria_label")  # type:ignore
                if field and field.json_schema_extra
                else None
            ),
            token=self.factory.token,
            value=value or None,
            error=form_errors.get(field_name),
        )

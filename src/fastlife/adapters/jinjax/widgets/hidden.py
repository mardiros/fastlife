"""Hidden fields"""

from fastlife.domain.model.types import Builtins

from .base import Widget


class HiddenWidget(Widget[Builtins]):
    '''
    Widget to annotate to display a field as an hidden field.

    ::
        from pydantic import BaseModel
        from fastlife.adapters.jinjax.widgets.base import CustomWidget
        from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget

        class MyForm(BaseModel):
            id: Annotated[str, CustomWidget(HiddenWidget)] = Field(...)
            """Identifier in the database."""

    '''

    template = """
    <Hidden :name="name" :value="value" :id="id" />
    """

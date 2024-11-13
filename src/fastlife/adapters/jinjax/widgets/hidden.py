"""Hidden fields"""

from fastlife.domain.model import Builtins
from .base import Widget


class HiddenWidget(Widget[str]):
    '''
    Widget to annotate to display a field as an hidden field.

    ::
        from pydantic import BaseModel
        from fastlife.adapters.jinjax.widgets.hidden import HiddenWidget

        class MyForm(BaseModel):
            id: Annotated[str, HiddenWidget] = Field(...)
            """Identifier in the database."""

    '''

    template = """
    <Hidden :name="name" :value="value" :id="id" />
    """

from typing import Annotated

from fastapi import Depends

from fastlife.adapters.fastapi.request import Request
from fastlife.service.translations import Localizer as RequestLocalizer


def get_localizer(request: Request) -> RequestLocalizer:
    """Return the localizer for the given request."""
    return request.registry.localizer(request.locale_name)


Localizer = Annotated[RequestLocalizer, Depends(get_localizer)]
"""Define a localizer"""

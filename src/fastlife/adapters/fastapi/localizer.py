from typing import Annotated

from fastapi import Depends

from fastlife.request.request import Request
from fastlife.services.translations import Localizer as RequestLocalizer


def get_localizer(request: Request) -> RequestLocalizer:
    return request.registry.localizer(request)


Localizer = Annotated[RequestLocalizer, Depends(get_localizer)]

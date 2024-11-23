from typing import Annotated

from fastapi import Depends

from fastlife.adapters.fastapi.request import Request
from fastlife.service.translations import Localizer as RequestLocalizer


def get_localizer(request: Request) -> RequestLocalizer:
    return request.registry.localizer(request)


Localizer = Annotated[RequestLocalizer, Depends(get_localizer)]

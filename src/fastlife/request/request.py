"""HTTP Request representation in a python object."""

from typing import Annotated, Any

from fastapi import Request as FastAPIRequest
from fastapi.params import Depends

from fastlife.config.registry import DefaultRegistry
from fastlife.domain.model.request import GenericRequest


def get_request(request: FastAPIRequest) -> GenericRequest[Any]:
    return request  # type: ignore


Request = Annotated[GenericRequest[DefaultRegistry], Depends(get_request)]
"""A request that is associated to the default registry."""
# FastAPI handle its Request objects using a lenient_issubclass,
# basically a issubclass(Request), doe to the Generic[T], it does not work.


AnyRequest = Annotated[GenericRequest[Any], Depends(get_request)]
"""A request version that is associated to the any registry."""


def get_registry(request: Request) -> DefaultRegistry:
    return request.registry


Registry = Annotated[DefaultRegistry, Depends(get_registry)]
"""FastAPI dependency to access to the registry."""

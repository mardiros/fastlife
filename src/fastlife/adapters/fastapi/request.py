"""HTTP Request representation in a python object."""

from typing import Annotated, Any

from fastapi import Request as FastAPIRequest
from fastapi.params import Depends

from fastlife.domain.model.request import GenericRequest
from fastlife.service.registry import DefaultRegistry


def get_request(request: FastAPIRequest) -> GenericRequest[Any, Any, Any]:
    """Return the Fastlife Request object."""
    return request  # type: ignore


Request = Annotated[GenericRequest[DefaultRegistry, Any, Any], Depends(get_request)]
"""A request that is associated to the default registry."""
# FastAPI handle its Request objects using a lenient_issubclass,
# basically a issubclass(Request), does not work with Generic[T].


AnyRequest = Annotated[GenericRequest[Any, Any, Any], Depends(get_request)]
"""A request version that is associated to the any registry."""


def get_registry(request: Request) -> DefaultRegistry:
    """Return the Fastlife Registry object."""
    return request.registry


Registry = Annotated[DefaultRegistry, Depends(get_registry)]
"""FastAPI dependency to access to the global registry."""

"""ASGI types from Starlette."""

from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

ASGIRequest = Request
"""Starlette request class used as ASGI Protocol base HTTP Request representation."""

ASGIResponse = Response
"""Starlette request class used as ASGI Protocol base HTTP Response representation."""

__all__ = [
    "ASGIApp",
    "ASGIRequest",
    "ASGIResponse",
    "Message",
    "Receive",
    "Scope",
    "Send",
]

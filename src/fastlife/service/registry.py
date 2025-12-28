"""Application registry."""

from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from fastapi import FastAPI

if TYPE_CHECKING:
    from fastlife.service.locale_negociator import LocaleNegociator  # coverage: ignore
    from fastlife.service.request_factory import RequestFactory  # coverage: ignore
    from fastlife.service.templates import (  # coverage: ignore
        AbstractTemplateRendererFactory,  # coverage: ignore
    )  # coverage: ignore
    from fastlife.service.translations import LocalizerFactory  # coverage: ignore

from fastlife.domain.model.template import InlineTemplate
from fastlife.settings import Settings

TSettings = TypeVar("TSettings", bound=Settings, covariant=True)
"""
A TypeVar used to override the DefaultRegistry to add more helpers in the registry.
"""


class GenericRegistry(Generic[TSettings]):
    """
    Application registry for fastlife dependency injection.
    It is initialized by the configurator and accessed by the `fastlife.Registry`.
    """

    settings: TSettings
    """Application settings."""
    renderers: Mapping[type[InlineTemplate], "AbstractTemplateRendererFactory[Any]"]
    """Registered template engine."""
    locale_negociator: "LocaleNegociator"
    """Used to fine the best language for the response."""
    localizer: "LocalizerFactory"
    """Used to localized message."""
    request_factory: "RequestFactory"

    def __init__(self, settings: TSettings) -> None:
        from fastlife.service.job import JobScheduler
        from fastlife.service.locale_negociator import default_negociator
        from fastlife.service.request_factory import default_request_factory
        from fastlife.service.translations import LocalizerFactory

        self.settings = settings
        self.locale_negociator = default_negociator(self.settings)
        self.renderers = {}
        self.localizer = LocalizerFactory()
        self.request_factory = default_request_factory(self)
        self.job_scheduler = JobScheduler(self)

    def get_renderer(
        self, template: InlineTemplate
    ) -> "AbstractTemplateRendererFactory[Any]":
        for cls in template.__class__.__mro__:
            if cls in self.renderers:
                return self.renderers[cls]
        raise RuntimeError(
            f"No renderer registered for template {template.__class__.__qualname__}"
        )

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncIterator[Any]:
        """
        The [lifespan](https://asgi.readthedocs.io/en/latest/specs/lifespan.html)
        is used to start the job scheduler.

        In fastlife the application state is the registry, it has to be overriden
        to add an implementation.
        """
        self.job_scheduler.start()
        yield
        # FIXME: make the wait statement comming from the settings
        self.job_scheduler.shutdown(wait=True)


DefaultRegistry = GenericRegistry[Settings]
"""
The default registry until you need to inject more component in the registry.
"""


TRegistry = TypeVar("TRegistry", bound=DefaultRegistry, covariant=True)
"""
A TypeVar used to override the DefaultRegistry to add more helpers in the registry.
"""

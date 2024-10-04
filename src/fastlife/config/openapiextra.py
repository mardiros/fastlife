"""Types for OpenAPI documentation."""

from pydantic import BaseModel, Field


class ExternalDocs(BaseModel):
    """OpenAPI externalDocs object."""

    description: str
    """link's description."""
    url: str
    """link's URL."""


class OpenApiTag(BaseModel):
    """OpenAPI tag object."""

    name: str
    """name of the tag."""
    description: str
    """explanation of the tag."""
    external_docs: ExternalDocs | None = Field(alias="externalDocs", default=None)
    """external link to the doc."""

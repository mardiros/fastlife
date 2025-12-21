import re
from collections.abc import Iterator, Mapping
from typing import Any

import bs4
import pytest
from fastapi import Request as FastApiRequest
from xcomponent import Catalog

from fastlife.adapters.fastapi.routing.router import Router
from fastlife.config.configurator import Configurator
from fastlife.domain.model.request import GenericRequest
from fastlife.settings import Settings
from fastlife.shared_utils.resolver import resolve


@pytest.fixture(autouse=True, scope="session")
def configurator() -> Configurator:
    # load the components
    cfg = Configurator(Settings())
    cfg.include("fastlife.adapters.xcomponent.functions")
    cfg.include("fastlife.adapters.xcomponent.html")
    cfg.include("fastlife.adapters.xcomponent.icons")
    return cfg


@pytest.fixture(autouse=True, scope="session")
def catalog(configurator: Configurator) -> Catalog:
    return configurator.build_catalogs()["app"]


@pytest.fixture()
def dummy_request(
    configurator: Configurator,
) -> GenericRequest[Any, Any, Any]:
    scope = {
        "type": "http",
        "headers": [("user-agent", "Mozilla/5.0"), ("accept", "text/html")],
        "router": Router(),
        "query_string": b"",
        "scheme": "http",
        "server": ("testserver", 80),
        "path": "/",
    }
    req = GenericRequest[Any, Any, Any](configurator.registry, FastApiRequest(scope))
    req.csrf_token.value = "CsRfT"
    return req


@pytest.fixture()
def globals(settings: Settings, dummy_request: Any) -> Mapping[str, str]:
    globs = resolve(settings.xcomponent_global_catalog_class)().model_dump()
    globs["request"] = dummy_request
    return globs


@pytest.fixture()
def soup_rendered(
    template_string: str,
    globals: Mapping[str, str],
    catalog: Catalog,
) -> Iterator[bs4.PageElement]:
    rendered = catalog.render(template_string.strip(), globals=globals)
    rendered = re.sub(r">\s+<", "><", rendered).strip()
    soup = bs4.BeautifulSoup(rendered, "html.parser")
    try:
        yield next(soup.children)  # type: ignore
    except Exception as exc:
        # Display the error in the assertion is a compromise
        yield exc  # type: ignore


@pytest.fixture()
def soup_expected(expected_string: str) -> bs4.PageElement:
    expected_string = re.sub(r">\s+<", "><", expected_string).strip()
    expected_soup = bs4.BeautifulSoup(expected_string.strip(), features="html.parser")
    return next(expected_soup.children)  # type: ignore

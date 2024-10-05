import sys
from collections.abc import Mapping
from pathlib import Path
from types import ModuleType
from typing import Any, Union, get_origin

import pytest

import fastlife.middlewares
import fastlife.middlewares.base
from fastlife import Configurator
from fastlife.shared_utils import resolver


def test_resolve():
    ConfiguratorClass = resolver.resolve("fastlife:Configurator")
    assert ConfiguratorClass is Configurator


@pytest.mark.parametrize(
    "params",
    [
        {"value": "xxx:xxx", "error": "Module xxx not found"},
        {
            "value": "fastlife:xxx",
            "error": "Attribute xxx not found in module fastlife",
        },
    ],
)
def test_resolve_error(params: Mapping[str, Any]):
    with pytest.raises(ValueError) as ctx:
        resolver.resolve(params["value"])
    assert str(ctx.value) == params["error"]


def test_resolve_extended():
    UnionType = resolver.resolve_extended(
        "tests.fastlife_app.models:Email|tests.fastlife_app.models:PhoneNumber"
    )
    assert get_origin(UnionType) == Union
    assert len(UnionType.__args__) == 2
    assert UnionType.__args__[0].__module__ == "tests.fastlife_app.models"
    assert UnionType.__args__[0].__name__ == "Email"
    assert UnionType.__args__[1].__module__ == "tests.fastlife_app.models"
    assert UnionType.__args__[1].__name__ == "PhoneNumber"


def test_resolve_path(root_dir: Path):
    path = resolver.resolve_path("fastlife:components")
    assert path == str(root_dir / "src" / "fastlife" / "components")


def test_resolve_path_error(root_dir: Path):
    with pytest.raises(ValueError) as err:
        resolver.resolve_path("xxx:templates")
    assert str(err.value) == "xxx:templates not found"


@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param(fastlife.middlewares, fastlife.middlewares, id="regular package"),
        pytest.param(fastlife.middlewares.base, fastlife.middlewares, id="module"),
        pytest.param(sys, sys, id="compiled package")
    ],
)
def test_resolve_package(input: ModuleType, expected: ModuleType):
    assert resolver.resolve_package(input) is expected

from pathlib import Path
from typing import Union, get_origin

from fastlife import Configurator
from fastlife.shared_utils import resolver


def test_resolve():
    ConfiguratorClass = resolver.resolve("fastlife:Configurator")
    assert ConfiguratorClass is Configurator


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
    path = resolver.resolve_path("fastlife:templates")
    assert path == str(root_dir / "src" / "fastlife" / "templates")

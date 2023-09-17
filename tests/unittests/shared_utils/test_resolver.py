from pathlib import Path

from fastlife import Configurator
from fastlife.shared_utils import resolver


def test_resolve():
    ConfiguratorClass = resolver.resolve("fastlife:Configurator")
    assert ConfiguratorClass is Configurator


def test_resolve_path(root_dir: Path):
    path = resolver.resolve_path("fastlife:templates")
    assert path == str(root_dir / "src" / "fastlife" / "templates")

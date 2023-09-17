import os
from pathlib import Path

import pytest


@pytest.fixture()
def root_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def python_path(root_dir: Path) -> None:
    os.environ["PYTHONPATH"] = str(root_dir / "tests")

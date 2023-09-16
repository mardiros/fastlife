import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def python_path():
    os.environ["PYTHONPATH"] = str(Path(__file__).parent)

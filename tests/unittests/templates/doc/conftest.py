from pathlib import Path

import pytest

from fastlife import GenericRequest
from tests.fastlife_app.config import MyRegistry, MySettings

Request = GenericRequest[None, MyRegistry]


@pytest.fixture(scope="session")
def components_dir() -> Path:
    return Path(__file__).parent / "components"


@pytest.fixture()
def settings(components_dir: Path) -> MySettings:
    return MySettings(template_search_path=f"{components_dir!s}")

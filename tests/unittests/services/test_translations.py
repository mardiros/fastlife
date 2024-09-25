from pathlib import Path

from fastlife.services.translations import LocalizerFactory, find_mo_files
from fastlife.shared_utils.resolver import resolve_path


def test_find_mo_files():
    root_path = resolve_path("tests.fastlife_app:locales")
    list_of_mo = set(find_mo_files(root_path))
    assert list_of_mo == {
        (
            "en",
            "fastlife_test",
            Path(root_path) / "en" / "LC_MESSAGES" / "fastlife_test.mo",
        ),
        (
            "en",
            "form_error",
            Path(root_path) / "en" / "LC_MESSAGES" / "form_error.mo",
        ),
        (
            "fr",
            "fastlife_test",
            Path(root_path) / "fr" / "LC_MESSAGES" / "fastlife_test.mo",
        ),
        (
            "fr",
            "form_error",
            Path(root_path) / "fr" / "LC_MESSAGES" / "form_error.mo",
        ),
    }


def test_load():
    factory = LocalizerFactory()
    factory.load("tests.fastlife_app:locales")
    assert set(factory._translations.keys()) == {"en", "fr"}  # type: ignore

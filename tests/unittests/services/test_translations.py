from pathlib import Path

from fastlife.service.translations import (
    LocalizerFactory,
    MergedTranslations,
    find_mo_files,
)
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
    assert set(
        factory._translations.translations.keys(),  # type: ignore
    ) == {"en", "fr"}


class DummyTranslations:
    def __init__(self) -> None:
        self._catalog = {"a": "A"}

    def plural(self, i: int) -> int:
        return int(i > 1)


def test_merged_translation():
    trans = MergedTranslations()
    assert trans._catalog == {}  # type: ignore
    assert trans.plural(0) == 1
    assert trans.plural(1) == 0
    assert trans.plural(2) == 1

    trans.merge(DummyTranslations())  # type: ignore
    assert trans.plural(0) == 0
    assert trans.plural(1) == 0
    assert trans.plural(2) == 1

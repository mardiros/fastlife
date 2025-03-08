"""Implement i18n."""

import pathlib
from collections import defaultdict
from collections.abc import Callable, Iterator
from gettext import GNUTranslations
from io import BufferedReader

from fastlife.shared_utils.resolver import resolve_path

LocaleName = str
Domain = str
CONTEXT_ENCODING = "%s\x04%s"


class TranslatableString(str):
    """
    Create a string made for translation associated to a domain.
    This class is instanciated by the
    {class}`fastlife.service.translations.TranslatableStringFactory` class.
    """

    __slots__ = ("domain",)

    def __new__(cls, msgid: str, domain: str) -> "TranslatableString":
        self = str.__new__(cls, msgid)
        self.domain = domain  # type: ignore
        return self


class TranslatableStringFactory:
    """Create a catalog of string associated to a domain."""

    def __init__(self, domain: str):
        self.domain = domain

    def __call__(self, msgid: str) -> str:
        """
        Use to generate the translatable string.

        usually:

        ```python
        _ = TranslatableStringFactory("mydomain")
        mymessage = _("translatable")
        ```

        Note that the string is associated to mydomain, so the babel extraction has
        to be initialized with that particular domain.
        """
        return TranslatableString(msgid, self.domain)


def find_mo_files(root_path: str) -> Iterator[tuple[LocaleName, Domain, pathlib.Path]]:
    """
    Find .mo files in a locales directory.

    :param root_path: locales directory.
    :return: a tupple containing locale_name, domain, file.
    """
    root = pathlib.Path(root_path)

    for locale_dir in root.iterdir():
        lc_messages_dir = locale_dir / "LC_MESSAGES"
        if not (locale_dir.is_dir() and lc_messages_dir.is_dir()):
            continue

        for mo_file in lc_messages_dir.glob("*.mo"):
            yield locale_dir.name, mo_file.stem, mo_file


def _default_plural(n: int) -> int:
    return int(n != 1)  # germanic plural by default


class MergedTranslations(GNUTranslations):
    _catalog: dict[str, str]

    def __init__(self) -> None:
        super().__init__()
        self._catalog = {}
        self.plural: Callable[[int], int] = _default_plural

    def merge(self, other: GNUTranslations) -> None:
        if hasattr(other, "_catalog"):
            self._catalog.update(other._catalog)  # type: ignore
        if hasattr(other, "plural"):
            self.plural = other.plural  # type: ignore


class Localizer:
    def __init__(self) -> None:
        self.translations: dict[Domain, MergedTranslations] = defaultdict(
            MergedTranslations
        )
        self.global_translations = MergedTranslations()

    def register(self, domain: str, file: BufferedReader) -> None:
        trans = GNUTranslations(file)
        self.translations[domain].merge(trans)
        self.global_translations.merge(trans)

    def __call__(self, message: str, mapping: dict[str, str] | None = None) -> str:
        return self.gettext(message, mapping)

    def gettext(self, message: str, mapping: dict[str, str] | None = None) -> str:
        if isinstance(message, TranslatableString):
            ret = self.translations[message.domain].gettext(message)  # type: ignore
        else:
            ret = self.global_translations.gettext(message)
        if mapping:
            ret = ret.format(**mapping)
        return ret

    def ngettext(
        self, singular: str, plural: str, n: int, mapping: dict[str, str] | None = None
    ) -> str:
        ret = self.global_translations.ngettext(singular, plural, n)
        mapping_num = {"num": n, **(mapping or {})}
        return ret.format(**mapping_num)

    def dgettext(
        self, domain: str, message: str, mapping: dict[str, str] | None = None
    ) -> str:
        ret = self.translations[domain].gettext(message)
        if mapping:
            ret = ret.format(**mapping)
        return ret

    def dngettext(
        self,
        domain: str,
        singular: str,
        plural: str,
        n: int,
        mapping: dict[str, str] | None = None,
    ) -> str:
        ret = self.translations[domain].ngettext(singular, plural, n)
        mapping_num = {"num": n, **(mapping or {})}
        return ret.format(**mapping_num)

    def pgettext(
        self, context: str, message: str, mapping: dict[str, str] | None = None
    ) -> str:
        ret = self.global_translations.pgettext(context, message)
        if mapping:
            ret = ret.format(**mapping)
        return ret

    def dpgettext(
        self,
        domain: str,
        context: str,
        message: str,
        mapping: dict[str, str] | None = None,
    ) -> str:
        ret = self.translations[domain].pgettext(context, message)
        if mapping:
            ret = ret.format(**mapping)
        return ret

    def npgettext(
        self,
        context: str,
        singular: str,
        plural: str,
        n: int,
        mapping: dict[str, str] | None = None,
    ) -> str:
        ret = self.global_translations.npgettext(context, singular, plural, n)
        mapping_num = {"num": n, **(mapping or {})}
        return ret.format(**mapping_num)

    def dnpgettext(
        self,
        domain: str,
        context: str,
        singular: str,
        plural: str,
        n: int,
        mapping: dict[str, str] | None = None,
    ) -> str:
        ret = self.translations[domain].npgettext(context, singular, plural, n)
        mapping_num = {"num": n, **(mapping or {})}
        return ret.format(**mapping_num)


class TranslationDictionary:
    def __init__(self) -> None:
        self.translations: dict[LocaleName, Localizer] = defaultdict(Localizer)

    def load(self, root_path: str) -> None:
        for locale_name, domain, file_ in find_mo_files(root_path):
            with file_.open("rb") as stream:
                self.translations[locale_name].register(domain, stream)

    def get(self, locale_name: LocaleName) -> Localizer:
        return self.translations[locale_name]

    def __contains__(self, other: LocaleName) -> bool:
        return other in self.translations


class LocalizerFactory:
    """Initialize the proper translation context per request."""

    def __init__(self) -> None:
        self._translations = TranslationDictionary()
        self.null_localizer = Localizer()

    def load(self, path: str) -> None:
        """
        load a translations from the model.
        :param path: a python module and the locales dir separated by a `:`
        """
        root_path = resolve_path(path)
        self._translations.load(root_path)

    def __call__(self, locale_name: LocaleName) -> Localizer:
        """Create the translation context for the given request."""
        if locale_name not in self._translations:
            return self.null_localizer
        return self._translations.get(locale_name)

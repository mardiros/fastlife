import pathlib
from typing import TYPE_CHECKING, Iterator, Tuple

from babel.support import NullTranslations, Translations

from fastlife.shared_utils.resolver import resolve_path

if TYPE_CHECKING:
    from fastlife import Request  # coverage: ignore

locale_name = str


def find_mo_files(root_path: str) -> Iterator[Tuple[str, str, pathlib.Path]]:
    root = pathlib.Path(root_path)

    # Walk through the directory structure and match the pattern
    for locale_dir in root.iterdir():
        if locale_dir.is_dir():  # Ensure it's a directory (locale)
            lc_messages_dir = locale_dir / "LC_MESSAGES"
            if lc_messages_dir.exists() and lc_messages_dir.is_dir():
                for mo_file in lc_messages_dir.glob("*.mo"):  # Find .mo files
                    yield locale_dir.name, mo_file.name[:-3], mo_file


class Localizer:
    def __init__(
        self, request: "Request", translations: Translations | NullTranslations
    ) -> None:
        self.locale_name = request.locale_name
        self.translations = translations

    def gettext(self, message: str, mapping: dict[str, str] | None = None) -> str:
        ret = self.translations.gettext(message)
        if mapping is not None:
            ret = ret.format(**mapping)
        return ret

    def ngettext(
        self, singular: str, plural: str, n: int, mapping: dict[str, str] | None = None
    ) -> str:
        ret = self.translations.ngettext(singular, plural, n)
        mapping_num = {"num": n, **(mapping or {})}
        return ret.format(**mapping_num)

    def dgettext(
        self, domain: str, message: str, mapping: dict[str, str] | None = None
    ) -> str:
        ret = self.translations.dgettext(domain, message)
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
        ret = self.translations.dngettext(domain, singular, plural, n)
        mapping_num = {"num": n, **(mapping or {})}
        return ret.format(**mapping_num)

    def pgettext(
        self, context: str, message: str, mapping: dict[str, str] | None = None
    ) -> str:
        ret = str(self.translations.pgettext(context, message))
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
        ret = str(self.translations.dpgettext(domain, context, message))
        if mapping:
            ret = ret.format(**mapping)
        return ret

    def dnpgettext(
        self,
        domain: str,
        context: str,
        singular: str,
        plural: str,
        n: int,
        mapping: dict[str, str] | None = None,
    ) -> str:
        ret = self.translations.dnpgettext(domain, context, singular, plural, n)
        mapping_num = {"num": n, **(mapping or {})}
        return ret.format(**mapping_num)


class LocalizerFactory:
    """Initialize the proper translation context per request."""

    _translations: dict[locale_name, Translations]

    def __init__(self) -> None:
        self._translations = {}

    def load(self, path: str) -> None:
        """
        load a translations from the model.
        :param path: a python module and the locales dir separated by a `:`
        """
        root_path = resolve_path(path)
        for locale_name, domain, file_ in find_mo_files(root_path):
            with file_.open("rb") as f:
                t = Translations(f, domain)
                if locale_name not in self._translations:
                    self._translations[locale_name] = Translations()
                self._translations[locale_name].add(t)
                self._translations[locale_name].merge(t)

    def __call__(self, request: "Request") -> Localizer:
        """Create the translation context for the given request."""
        trans: Translations | NullTranslations | None = self._translations.get(
            request.locale_name
        )
        if not trans:
            trans = self._translations.get(request.registry.settings.default_locale)
        if not trans:
            trans = NullTranslations()
        return Localizer(request, trans)

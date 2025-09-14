"""Use ``<Icon>`` to load icons."""

import html
import re
from functools import cache
from importlib import util
from pathlib import Path
from typing import Literal
from zipfile import ZipFile

from fastlife.adapters.xcomponent.catalog import catalog


@cache
def icon_path() -> Path:
    spec = util.find_spec("heroicons")
    if spec is None or spec.origin is None:
        raise ValueError("Install heroicons first")  # coverage: ignore
    return Path(spec.origin).parent


@cache
def get_from_zip(
    name: str,
    mode: str,
) -> str | None:
    iconzip = icon_path() / "heroicons.zip"
    with ZipFile(iconzip, "r") as zip_ref:
        file_list = zip_ref.namelist()
        for filepath in file_list:
            if filepath == f"{mode}/{name}.svg":
                with zip_ref.open(filepath) as file:
                    return file.read().decode("utf-8")
    return None


@catalog.function
def load_icon(
    name: str,
    mode: str,
    id: str | None = None,
    title: str | None = None,
    class_: str | None = None,
) -> str:
    """
    Function to load the icon behind the scene for  the ``<Icon>`` component.

    :param name: name of the icon.
    :param mode: mode of the hero icon.
    :param id: dom unique identifier.
    :param title: title that can be bubble to the icon.
    :param class_: css class to set.
    """
    icon = get_from_zip(name, mode)
    if not icon:
        return ""

    attrs = ""
    if id:
        attrs += f' id="{html.escape(id)}"'
    if class_:
        attrs += f' class="{html.escape(class_)}"'
    if attrs:
        icon = icon.replace(' viewBox="', f'{attrs} viewBox="', 1)
    if title:
        icon = re.sub(
            r"(<path[^>]*?)/>",
            rf"\1><title>{html.escape(title)}</title></path>",
            icon,
        )
    return icon


@catalog.component
def Icon(
    name: str,
    mode: Literal["micro", "mini", "outline", "solid"] = "solid",
    id: str | None = None,
    title: str | None = None,
    class_: str | None = None,
) -> str:
    """
    Add an icon from hero icon package. The svg is already injected to the DOM.

    :param name: name of the icon.
    :param mode: mode of the hero icon.
    :param id: dom unique identifier.
    :param title: title that can be bubble to the icon.
    :param class_: css class to set.
    """
    return """
    <>{load_icon(name, mode, id, title, class_)}</>
    """

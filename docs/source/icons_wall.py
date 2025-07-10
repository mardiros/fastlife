import textwrap
from pathlib import Path
from typing import IO
from collections.abc import Iterator

from sphinx.application import Sphinx
from zipfile import ZipFile

from fastlife.adapters.xcomponent.icons.icons import icon_path, Icon


def intro():
    return """
    <p>
        Fastlife comes with a set of icons that comes from
        <a href="https://heroicons.com/">heroicons</a>
        (MIT License - Copyright (c) Tailwind Labs, Inc.).

        You must install the extra dependency heroicons.
    </p>
    <p>
        Available icons, click to copy.
    </p>

    <script>
        function copyText(text) {
            const textarea = document.createElement('textarea');
            textarea.value = '<Icon name="' + text + '" />';
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
        }
    </script>
    """


def iter_zip(mode: str = "solid") -> Iterator[str]:
    iconzip = icon_path() / "heroicons.zip"
    with ZipFile(iconzip, "r") as zip_ref:
        file_list = zip_ref.namelist()
        for filepath in file_list:
            if filepath.startswith(f"{mode}/"):
                name = filepath.split("/", 1)[1].rsplit(".", 1)[0]
                yield name


def write_icons(file: IO[str]):
    for name in iter_zip():
        out = (
            '<div class="flex flex-col items-center text-center cursor-pointer" '
            f"onclick=\"copyText('{name}')\">\n"
        )
        out += Icon(name, class_="w-16 h-16", title=name).replace("\n", "    \n")
        out += f'<div>&lt;Icon name="{name}" /&gt;</div>'
        out += "</div>\n"
        file.write(textwrap.indent(out, prefix="    "))


def generate_page(app: Sphinx) -> None:
    outdir: Path = Path(app.srcdir) / app.config.icon_wall_output_dir  # type: ignore
    with open(outdir / "icons.rst", "w") as wf:
        wf.write("Icons\n")
        wf.write("-----\n")
        wf.write(".. raw:: html\n\n")
        wf.write(intro())
        wf.write("    <style>\n")
        wf.write(
            textwrap.indent(
                (outdir / "iconwall.css").read_text(),
                prefix="    ",
            )
        )
        wf.write("    </style>\n")
        wf.write('    <div class="grid grid-cols-2 gap-4 p-6">')
        write_icons(wf)
        wf.write("    </div>")


def setup(app: Sphinx) -> None:
    app.add_config_value("icon_wall_output_dir", "iconswall", "env")
    app.connect("builder-inited", generate_page)

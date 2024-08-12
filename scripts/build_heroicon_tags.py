#!/usr/bin/env python

import sys
from collections import defaultdict
from importlib import util
from pathlib import Path
from textwrap import dedent
from typing import Iterator, Tuple
from zipfile import ZipFile

package_name = "heroicons"
root_dir = Path(__file__).parents[1]


def to_name(filename: str) -> str:
    ret = "".join([c.capitalize() for c in filename[:-4].split("-")])
    if ret[0].isdigit():
        ret = f"Hero{ret}"
    return ret


def add_attrs(content: str) -> str:
    return content.replace('viewBox="', 'class="{{attrs.class or \'\'}}" viewBox="')


def iter_zip(heroicons_path: Path) -> Iterator[Tuple[str, str]]:
    iconzip = heroicons_path / "heroicons.zip"
    with ZipFile(iconzip, "r") as zip_ref:
        file_list = zip_ref.namelist()
        for filepath in file_list:
            with zip_ref.open(filepath) as file:
                content = file.read().decode("utf-8")
                yield filepath, content


def main():
    spec = util.find_spec(package_name)
    if spec is None or spec.origin is None:
        print(f"Package {package_name} is probably not installed", file=sys.stderr)
        sys.exit(-1)

    iconsdir = root_dir / "src" / "fastlife" / "templates" / "icons"

    heroicons_path = Path(spec.origin).parent
    names: dict[str, set[str]] = defaultdict(set)
    for filepath, content in iter_zip(heroicons_path):
        dir_, name = filepath.split("/")

        if not name.endswith(".svg"):
            continue

        icondir = iconsdir / dir_
        icondir.mkdir(parents=True, exist_ok=True)
        (icondir / f"{to_name(name)}.jinja").write_text(add_attrs(content))
        names[to_name(name)].add(dir_)

    for name, vals in names.items():
        modes = sorted(vals)
        components: list[str] = []
        for idx, mode in enumerate(modes):
            if idx == 0:
                if_stmt = f'{{% if mode == "{mode}"%}}'
            else:
                if_stmt = f'{{% elif mode == "{mode}"%}}'
            components.append(
                f"{if_stmt}<icons.{mode}.{name} :class=\"attrs.class or ''\"/>\n",
            )

        stmt = f"{'                '.join(components)}                {{%endif%}}"

        (iconsdir / f"{name}.jinja").write_text(
            dedent(
                f"""\
                {{# def mode: Literal["{'","'.join(modes)}"] = "solid"  #}}

                {stmt}
                """,
            )
        )

    icons_wall = root_dir / "tests" / "fastlife_app" / "templates" / "IconsWall.jinja"
    icons_wall.unlink()
    with open(icons_wall, "w") as fw:
        fw.write("<Layout>\n")
        fw.write(
            """
            <script>
            function copyText(text) {
                const textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
            }
            </script>
        """
        )
        fw.write("<p>Available icons, click to copy</p>\n")

        fw.write('<div class="grid grid-cols-5 gap-4 p-6">\n')
        for name, vals in names.items():
            fw.write(
                '<div class="flex flex-col items-center text-center cursor-pointer" '
                f"onclick=\"copyText('&lt;{name} /&gt;')\">"
            )
            fw.write(f'<icons.{name} class="w-16 h-16" />\n')
            fw.write(f'<p class="mt-2">{name}</p>\n')
            fw.write("</div>\n")

        fw.write("</div>\n")
        fw.write("</Layout>\n")


if __name__ == "__main__":
    main()

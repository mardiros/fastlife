#!/usr/bin/env python

import re
import sys
from collections import defaultdict
from collections.abc import Iterator
from importlib import util
from pathlib import Path
from textwrap import dedent
from zipfile import ZipFile

package_name = "heroicons"
root_dir = Path(__file__).parents[1]


def to_name(filename: str) -> str:
    ret = "".join([c.capitalize() for c in filename[:-4].split("-")])
    if ret[0].isdigit():
        ret = f"Hero{ret}"
    return ret


def add_attrs(content: str) -> str:
    ret = dedent(
        """\
        {# def
            id: Annotated[str | "unique identifier of the element."] = None,
            title: Annotated[str | None, "title element of the svg"] = None,
            class_: Annotated[str | None, "css classapplide to the svg element"] = None,
        #}
        """
    ) + content.replace(
        'viewBox="',
        '{% if id %}id="{{id}}" {%endif%}class="{{attrs.class or \'\'}}" viewBox="',
    )
    ret = re.sub(
        r"(<path[^>]*?)/>",
        r"\1>{% if title %}<title>{{title}}</title>{% endif %}</path>",
        ret,
    )
    return ret


def iter_zip(heroicons_path: Path) -> Iterator[tuple[str, str]]:
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

    iconsdir = root_dir / "src" / "fastlife" / "components" / "icons"

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
                f'{if_stmt}<icons.{mode}.{name} :id="id" '
                ':class="attrs.class or \'\'" :title="title" />\n',
            )

        stmt = f"{'                '.join(components)}                {{%endif%}}"

        (iconsdir / f"{name}.jinja").write_text(
            dedent(
                f"""\
                {{# def
                    id: Annotated[str | None, "identifier of the element."] = None,
                    title: Annotated[str | None, "title element of the svg"] = None,
                    class_: Annotated[
                        str | None, "css class applied to the svg element"
                    ] = None,
                    mode: Literal["{'","'.join(modes)}"] = "solid"
                #}}

                {stmt}
                """,
            )
        )

    icons_wall = root_dir / "tests" / "fastlife_app" / "templates" / "IconsWall.jinja"
    icons_wall.unlink(missing_ok=True)
    icons_wall.parent.mkdir(exist_ok=True)
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
        for name in names:
            fw.write(
                '<div class="flex flex-col items-center text-center cursor-pointer" '
                f"onclick=\"copyText('&lt;icons.{name} /&gt;')\">"
            )
            fw.write(f'<icons.{name} class="w-16 h-16" title="{name}" />\n')
            fw.write(f'<p class="mt-2">{name}</p>\n')
            fw.write("</div>\n")

        fw.write("</div>\n")
        fw.write("</Layout>\n")


if __name__ == "__main__":
    main()

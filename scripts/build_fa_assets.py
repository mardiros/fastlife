#!/usr/bin/env python

import re
import sys
from importlib import metadata, util
from pathlib import Path
from typing import Iterator

package_name = "fontawesomefree"
root_dir = Path(__file__).parents[1]

splitter = re.compile(r"\{|\}")


def yield_css_class(css_file: Path) -> Iterator[str]:
    css_content = css_file.read_text()
    css_content = css_content.split("*/", maxsplit=1).pop()
    splits = iter(splitter.split(css_content))

    while True:
        try:
            names = next(splits)
            content = next(splits)
            for name in names.split(","):
                name = name.strip()
                if name.endswith("before") and "content" in content:
                    yield name.split(":").pop(0).lstrip(".")
        except StopIteration:
            return


def to_name(css: str) -> str:
    ret = "".join([c.capitalize() for c in css.split("-")[1:]])
    if ret[0].isdigit():
        ret = f"Fa{ret}"
    return ret


def to_content(*filenames: str, version: str, selector: str) -> Iterator[str]:
    yield '{# def mode: Literal["solid", "regular", "base"] = "solid" #}\n'
    yield '{#css "'
    for filename in filenames[:-1]:
        yield f"font-awesome/{version}/css/{filename},"
    yield f"font-awesome/{version}/css/{filenames[-1]}"
    yield " #}\n\n"
    yield "<i class=\"fa {% if mode == 'solid' %}fas {% elif mode=='regular' %}far "
    yield "{% else %}{% endif %}"
    yield f"{selector} {{{{attrs.class or ''}}}}\"></i>"


def write_fa(css_dir: Path, version: str) -> Iterator[str]:
    filename = "fontawesome.min.css"
    file = css_dir / filename
    dir = root_dir / "src" / "fastlife" / "templates" / "fa"
    dir.mkdir(parents=True, exist_ok=True)
    for selector in yield_css_class(file):
        name = to_name(selector)
        f = dir / f"{name}.jinja"
        f.write_text(
            "".join(
                to_content(
                    filename,
                    "solid.min.css",
                    "regular.min.css",
                    version=version,
                    selector=selector,
                )
            )
        )
        yield f"fa.{name}"


def to_content_brand(*filenames: str, version: str, selector: str) -> Iterator[str]:
    yield '{#css "'
    for filename in filenames[:-1]:
        yield f"font-awesome/{version}/css/{filename},"
    yield f"font-awesome/{version}/css/{filenames[-1]}"
    yield " #}\n"
    yield f"<i class=\"{selector} {{{{attrs.class or ''}}}}\"></i>"


def write_fa_brands(css_dir: Path, version: str) -> Iterator[str]:
    filename = "brands.min.css"
    file = css_dir / filename
    dir = root_dir / "src" / "fastlife" / "templates" / "fa" / "brands"
    dir.mkdir(parents=True, exist_ok=True)
    for selector in yield_css_class(file):
        name = to_name(selector)
        f = dir / f"{name}.jinja"
        f.write_text(
            "".join(
                to_content_brand(
                    "fontawesome.min.css",
                    filename,
                    version=version,
                    selector=f"fab {selector}",
                )
            )
        )
        yield f"fa.brands.{name}"


# def write_fa_duotone(css_dir: Path, version: str) -> Iterator[str]:
#     filename = "fontawesome.min.css"
#     file = css_dir / filename
#     dir = root_dir / "src" / "fastlife" / "templates" / "fa" / "duotone"
#     dir.mkdir(parents=True, exist_ok=True)
#     for selector in yield_css_class(file):
#         name = to_name(selector)
#         f = dir / f"{name}.jinja"
#         f.write_text(
#             "".join(
#                 to_content(
#                     "solid.min.css",
#                     "duotone.min.css",
#                     version=version,
#                     selector=f"fa-duotone {selector}",
#                 )
#             )
#         )
#         yield f"fa.duotone.{name}"


def main():
    try:
        version = metadata.version(package_name)
    except metadata.PackageNotFoundError:
        print(f"Package {package_name} is probably not installed", file=sys.stderr)
        sys.exit(-1)

    spec = util.find_spec(package_name)
    if spec is None or spec.origin is None:
        print(f"Package {package_name} is probably not installed", file=sys.stderr)
        sys.exit(-1)
    fontawesome_path = Path(spec.origin).parent
    css_dir = fontawesome_path / "static" / "fontawesomefree" / "css"

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
        for icon in write_fa(css_dir, version):
            fw.write(
                '<div class="text-center cursor-pointer" '
                f"onclick=\"copyText('&lt;{icon} /&gt;')\">"
            )
            fw.write(f"<{icon} class='fa-2x' />\n")
            fw.write(f'<p class="mt-2">{icon}</p>\n')
            fw.write("</div>\n")
            # fw.write(f"<{icon} mode='solid' class='fa-2x' /> solid {icon}<br/>\n")
            # fw.write(f"<{icon} mode='regular' class='fa-2x' /> regular {icon}<br/>\n")
        for icon in write_fa_brands(css_dir, version):
            fw.write('<div class="text-center">')
            fw.write(f"<{icon} class='fa-2x' />\n")
            fw.write(f'<p class="mt-2">{icon}</p>\n')
            fw.write("</div>\n")

        fw.write("</Layout>\n")


if __name__ == "__main__":
    main()

from pathlib import Path

import jinjax.catalog
from sphinx.application import Sphinx

from fastlife.adapters.jinjax.renderer import build_searchpath
from fastlife.shared_utils.resolver import resolve_path


def write_jinja(app: Sphinx) -> Path:
    iconsdir = Path(resolve_path("fastlife:components")) / "icons"

    outdir = Path(app.srcdir) / app.config.icon_wall_output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    icons_wall: Path = outdir / "IconsWall.jinja"
    icons_wall.unlink(missing_ok=True)
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

        fw.write('<div class="grid grid-cols-2 gap-4 p-6">\n')
        for file in iconsdir.glob("*.jinja"):
            name = file.name[: -len(".jinja")]
            fw.write(
                '<div class="flex flex-col items-center text-center cursor-pointer" '
                f"onclick=\"copyText('&lt;icons.{name} /&gt;')\">"
            )
            fw.write(f'<icons.{name} class="w-16 h-16" title="{name}" />\n')
            fw.write(f'<p class="mt-2">{name}</p>\n')
            fw.write("</div>\n")

        fw.write("</div>\n")
        fw.write("</Layout>\n")
    return icons_wall


def generate_page(app: Sphinx) -> None:
    tpl = write_jinja(app)
    outfile = tpl.parent / "icons.md"
    catalog = jinjax.catalog.Catalog(auto_reload=False)
    for p in build_searchpath(f"fastlife:components,{tpl.parent}"):
        catalog.add_folder(p)

    outfile.write_text(catalog.render("IconsWall"))


def setup(app: Sphinx) -> None:
    app.add_config_value("icon_wall_output_dir", "iconswall", "env")
    app.connect("builder-inited", generate_page)

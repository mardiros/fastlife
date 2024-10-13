import re
from pathlib import Path
from typing import IO

from sphinx.application import Sphinx

from fastlife.adapters.jinjax.jinjax_ext.inspectable_catalog import InspectableCatalog
from fastlife.adapters.jinjax.renderer import build_searchpath


def write_icons(fw: IO[str], catalog: InspectableCatalog):
    includes = [re.compile(r"^icons\.[a-zA-Z0-9]+$")]
    for component in catalog.iter_components(includes=includes):
        name = component.name
        fw.write(
            '<div class="flex flex-col items-center text-center cursor-pointer" '
            f"onclick=\"copyText('&lt;{name} /&gt;')\">"
        )
        fw.write(f'<{name} class="w-16 h-16" title="{name}" />\n')
        fw.write(
            component.build_docstring()
        )
        fw.write("\n</div>\n")


def write_jinja(app: Sphinx, catalog: InspectableCatalog, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    icons_wall: Path = outdir / "IconsWall.jinja"
    icons_wall.unlink(missing_ok=True)
    with open(icons_wall, "w") as fw:
        fw.write("<Layout>\n")

        fw.write('<div class="grid grid-cols-2 gap-4 p-6">\n')
        write_icons(fw, catalog)
        fw.write("</div>\n")
        fw.write("</Layout>\n")


def generate_page(app: Sphinx) -> None:
    catalog = InspectableCatalog(auto_reload=False)

    outdir = Path(app.srcdir) / app.config.icon_wall_output_dir

    for path in build_searchpath(f"fastlife:components,{outdir}"):
        catalog.add_folder(path)

    write_jinja(app, catalog, outdir)
    icons_wall = catalog.render("IconsWall")  # type: ignore
    outfile: Path = outdir / "icons.rst"
    with open(outfile, "w") as wf:
        wf.write("Icons\n")
        wf.write("-----\n")
        wf.write(".. raw:: html\n\n")
        lines = iter(icons_wall.split("\n"))
        while True:
            try:
                line = next(lines)
            except StopIteration:
                break

            if line.startswith(".. "):
                wf.write(f"{line}\n")
                line = next(lines)
                while len(line) == 0 or line.startswith("    "):
                    line = next(lines)

                wf.write(".. raw:: html\n\n")

            wf.write(f"    {line}\n")


def setup(app: Sphinx) -> None:
    app.add_config_value("icon_wall_output_dir", "iconswall", "env")
    app.connect("builder-inited", generate_page)

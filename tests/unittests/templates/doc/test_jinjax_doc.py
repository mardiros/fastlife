import pathlib
import tempfile
from collections.abc import Iterator

import bs4
import pytest
from sphinx.application import Sphinx


@pytest.fixture
def sphinx_app() -> Iterator[Sphinx]:
    # Create a temporary directory for the Sphinx output
    temp_out_dir = tempfile.TemporaryDirectory()
    temp_doctree_dir = tempfile.TemporaryDirectory()

    # Set up the paths for the Sphinx project
    src_dir = str(pathlib.Path(__file__).parent / "docs")
    conf_dir = src_dir  # Same as src_dir for simplicity

    # Initialize Sphinx application
    app = Sphinx(
        srcdir=src_dir,
        confdir=conf_dir,
        outdir=temp_out_dir.name,
        doctreedir=temp_doctree_dir.name,
        buildername="html",
    )

    yield app

    temp_out_dir.cleanup()
    temp_doctree_dir.cleanup()


def test_gen_doc(sphinx_app: Sphinx):
    sphinx_app.build()
    path = pathlib.Path(sphinx_app.outdir)
    assert path.exists()
    dummy_component = path / "components" / "HelloWorld.html"

    # print()
    # print(f"firefox {dummy_component}")
    # breakpoint()

    assert dummy_component.exists()
    assert (
        '<span class="jinjax-component-name"><span class="pre">HelloWorld</span></span>'
        in dummy_component.read_text()
    )

    html = bs4.BeautifulSoup(dummy_component.read_text(), "html.parser")
    signature = html.find(attrs={"jinjax-signature"})
    assert signature is not None
    assert (
        signature.get_text().strip() == "<HelloWorld person: "
        "fastlife_app.models.Person | None = None "
        "method: Literal['get', 'post'] = 'post' "
        "/>"
    )
    person = signature.find("a")
    assert isinstance(person, bs4.Tag)
    assert person.attrs["href"] == "../models.html#fastlife_app.models.Person"

    html = bs4.BeautifulSoup((path / "models.html").read_text(), "html.parser")

    person = html.find(attrs={"id": "person-class"})
    assert isinstance(person, bs4.Tag)
    person = person.find("dd")
    assert isinstance(person, bs4.Tag)
    assert person.get_text().startswith("A models to say hello in <HelloWorld/>")
    person = person.find("a")
    assert isinstance(person, bs4.Tag)
    assert person.attrs["href"] == "components/HelloWorld.html"

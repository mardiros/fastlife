import ast
import textwrap

import pytest

from fastlife.adapters.jinjax.jinjax_ext.docstring import generate_docstring


@pytest.mark.parametrize(
    "method,name,add_content,expected",
    [
        pytest.param(
            "def component(): ...", "Noop", False, "Noop()\n\n    \n", id="No param"
        ),
        pytest.param(
            "def component(): ...",
            "P",
            True,
            "P(content: Any)\n\n    :param content: child node.\n",
            id="has content",
        ),
        pytest.param(
            textwrap.dedent(
                """
                def component():
                    '''Paragraph'''
                """
            ),
            "P",
            False,
            textwrap.dedent(
                """\
                P()

                    Paragraph
                """
            ),
            id="has doc+content",
        ),
        pytest.param(
            textwrap.dedent(
                """
                def component():
                    '''Paragraph'''
                """
            ),
            "P",
            True,
            textwrap.dedent(
                """\
                P(content: Any)

                    Paragraph

                    :param content: child node.
                """
            ),
            id="has doc+content",
        ),
        pytest.param(
            textwrap.dedent(
                """
                def component(*, id: str):
                    '''Paragraph'''
                """
            ),
            "P",
            True,
            textwrap.dedent(
                """\
                P(id: str, content: Any)

                    Paragraph

                    :param id:
                    :param content: child node.
                """
            ),
            id="has doc+id+content",
        ),
        pytest.param(
            textwrap.dedent(
                """
                def component(*, id: Annotated[str, "uniq id"]):
                    '''Paragraph'''
                """
            ),
            "P",
            True,
            textwrap.dedent(
                """\
                P(id: str, content: Any)

                    Paragraph

                    :param id: uniq id
                    :param content: child node.
                """
            ),
            id="has doc+id annotated+content",
        ),
    ],
)
def test_build_docstring(method: str, name: str, add_content: bool, expected: str):
    meth = ast.parse(method).body[0]
    assert isinstance(meth, ast.FunctionDef)
    resp = generate_docstring(meth, name, add_content)
    assert resp == expected

# views.py
from pathlib import Path

from xcomponent import XNode

from fastlife import XTemplate, view_config, x_component

templates_dir = Path(__file__).parent


@x_component()
def Layout(children: XNode, title: str = "Hello World") -> str:
    return """
    <>
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8" />
                <title>{title}</title>
            </head>
            <body>
                {children}
            </body>
        </html>
    </>
    """


class HelloWorld(XTemplate):
    template = "<Layout>Hello World</Layout>"


@view_config("hello_world", "/")
async def hello_world() -> HelloWorld:
    return HelloWorld()

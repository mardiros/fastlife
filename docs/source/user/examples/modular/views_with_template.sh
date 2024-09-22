cat << 'EOF' > views.py
from typing import Annotated
from fastapi import Response
from fastlife import Configurator, Template, configure, template


async def hello_world(
    template: Annotated[Template, template("HelloWorld.jinja")],
):
    return template()


@configure
def includeme(config: Configurator) -> None:
    config.add_route("hello_world", "/", hello_world)
EOF

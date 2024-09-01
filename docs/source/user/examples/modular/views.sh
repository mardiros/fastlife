cat << 'EOF' > views.py
from fastlife import Configurator, configure


async def hello_world():
    return {"message": "Hello World"}


@configure
def includeme(config: Configurator) -> None:
    config.add_route("hello_world", "/", hello_world)
EOF

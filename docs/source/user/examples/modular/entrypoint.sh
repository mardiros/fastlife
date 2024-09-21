cat << 'EOF' > entrypoint.py
from fastlife import Configurator, Settings

def build_app():
    config = Configurator(Settings())
    config.include("views")
    return config.build_asgi_app()

app = build_app()
EOF

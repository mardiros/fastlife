from pathlib import Path

from fastlife.configurator import Configurator, configure

static_dir = Path(__file__).parent


@configure
def includeme(config: Configurator):
    config.add_static_route("/static/css", static_dir / "css", name="static")

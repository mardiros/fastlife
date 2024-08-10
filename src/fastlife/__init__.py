from .configurator import Configurator, configure
from .configurator.registry import Registry

from .monkeypatch import monkeypatch
# from .request.form_data import model
from .templating import Template, template

monkeypatch()

__all__ = [
    # Config
    "configure",
    "Configurator",
    "template",
    "Template",
    "Registry",
    # Model
    # "model",
]

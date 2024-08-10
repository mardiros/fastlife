import re
from jinjax import component


def monkeypatch() -> None:
    # the current regex is currently breaking the A component
    # and we don't use comments inside {# def #}
    component.RX_INTER_COMMENTS = re.compile("^$")

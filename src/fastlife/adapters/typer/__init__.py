"""
CLI Application Integration

FastLife provides a built-in CLI system designed for development and maintenance tasks.
This implementation extends Typer's functionality while integrating with FastLife's
configuration system and dependency registry.

Key Features:
- Seamless integration with FastLife's settings and service registry
- Asynchronous command support out of the box
- Configuration-driven CLI setup through FastLife's dependency system

The `AsyncTyper` class extends Typer to:
1. Automatically configure CLI applications using FastLife's settings
2. Enable native async command execution
3. Maintain compatibility with Typer's existing feature set
"""

from .cli import AsyncTyper

__all__ = ["AsyncTyper"]

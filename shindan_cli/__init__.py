""".. include:: ../README.md"""  # noqa: D400, D415

from __future__ import annotations

import importlib.metadata

from .shindan import ShindanError, ShindanResult, shindan

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ("ShindanError", "ShindanResult", "shindan")

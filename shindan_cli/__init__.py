"""Initialize shindan-cli package."""
from __future__ import annotations

from .shindan import ShindanError, ShindanResult, shindan

__version__ = "1.0.1"
__all__ = ("shindan", "ShindanResult", "ShindanError")

from __future__ import annotations

from pathlib import Path

from src.config import PROJECT_ROOT

__all__ = ["display_path"]


def display_path(path: str | Path) -> str:
    candidate = Path(path)
    try:
        return str(candidate.resolve().relative_to(PROJECT_ROOT.resolve()))
    except (OSError, RuntimeError, ValueError):
        return candidate.name or str(candidate)

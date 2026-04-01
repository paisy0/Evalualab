from __future__ import annotations

from pathlib import Path, PureWindowsPath

from src.config import PROJECT_ROOT

__all__ = ["display_path"]


def _filename(path: str | Path) -> str:
    """Extract the filename from *path*, regardless of the platform the
    path was created on.  ``PureWindowsPath`` understands both ``\\``
    and ``/`` separators, so it works for Windows paths on Linux too."""
    return PureWindowsPath(str(path)).name or str(path)


def display_path(path: str | Path) -> str:
    candidate = Path(path)
    try:
        rel = str(candidate.resolve().relative_to(PROJECT_ROOT.resolve()))
    except (OSError, RuntimeError, ValueError):
        return _filename(path)

    # On Linux a Windows-style path like "C:\\Users\\...\\file.txt" is
    # not recognised as absolute so resolve() prepends the CWD.
    # relative_to() then succeeds but returns the raw Windows string.
    # Detect this and fall back to filename-only.
    if "\\" in rel:
        return _filename(path)
    return rel

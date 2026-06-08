from __future__ import annotations

from pathlib import Path
import re

__all__ = ["__version__"]


def _read_version_from_pyproject() -> str:
    project_root = Path(__file__).resolve().parent.parent
    pyproject = project_root / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise RuntimeError("Unable to read version from pyproject.toml")
    return match.group(1)


__version__ = _read_version_from_pyproject()
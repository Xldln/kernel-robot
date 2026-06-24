"""Auto-detect the project root, resolving paths correctly on both host and Docker.

Usage:
  from mindbridge.src.core.config.paths import PROJECT_ROOT, resolve, resolve_config_paths

  # Resolve a single path string (replaces /workspace/ with actual PROJECT_ROOT)
  model_dir = resolve("/workspace/mindbridge/models/sam3-main")

  # Resolve all path-like values in a loaded YAML config dict (recursive, in-place)
  cfg = yaml.safe_load(f)
  resolve_config_paths(cfg)
"""

from __future__ import annotations

import os
from pathlib import Path


def _find_project_root() -> Path:
    """Find git repo root or fall back to a well-known marker."""
    env_root = os.environ.get("PROJECT_ROOT", "")
    if env_root:
        p = Path(env_root).expanduser().resolve()
        if p.is_dir():
            return p

    # Walk up from this file: mindbridge/src/core/config/paths.py → project root
    p = Path(__file__).resolve().parent  # config/
    for _ in range(4):
        p = p.parent
    if (p / ".git").exists():
        return p

    # Docker fallback
    if Path("/workspace").is_dir():
        return Path("/workspace")

    # Final fallback — assume we're inside the repo
    return p


PROJECT_ROOT = _find_project_root()


def resolve(path: str) -> str:
    """Replace /workspace/ prefix with the actual PROJECT_ROOT."""
    s = path.replace("/workspace/", f"{PROJECT_ROOT}/")
    s = os.path.expandvars(s)
    return str(Path(s).expanduser())


def resolve_config_paths(cfg: dict) -> None:
    """Recursively resolve path values in a loaded config dict (mutates in-place).

    Any string value containing '/workspace/' or '/models/' is treated as a path
    and resolved against PROJECT_ROOT.
    """
    _resolve_dict(cfg)


def _resolve_dict(d: dict) -> None:
    for key, value in d.items():
        if isinstance(value, str):
            if "/workspace/" in value or "/models/" in value:
                d[key] = resolve(value)
        elif isinstance(value, dict):
            _resolve_dict(value)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, str) and ("/workspace/" in item or "/models/" in item):
                    value[i] = resolve(item)
                elif isinstance(item, dict):
                    _resolve_dict(item)

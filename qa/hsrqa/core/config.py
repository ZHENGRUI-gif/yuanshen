from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _expand_vars(value: str) -> str:
    # Expand %VAR% and $VAR styles.
    return os.path.expandvars(value)


def _walk_expand(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _walk_expand(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_expand(v) for v in obj]
    if isinstance(obj, str):
        return _expand_vars(obj)
    return obj


@dataclass(frozen=True)
class Config:
    raw: dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)


def load_config(path: Path) -> Config:
    data = json.loads(path.read_text(encoding="utf-8"))
    data = _walk_expand(data)
    return Config(raw=data)


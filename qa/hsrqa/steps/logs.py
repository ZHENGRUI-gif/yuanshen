from __future__ import annotations

import fnmatch
import os
import re
import shutil
from pathlib import Path
from typing import Any, Iterable

from hsrqa.core.config import Config


def _iter_files(roots: list[str], include_globs: list[str]) -> Iterable[Path]:
    for root in roots:
        root_path = Path(root)
        if not root_path.exists():
            continue
        for p in root_path.rglob("*"):
            if not p.is_file():
                continue
            if any(fnmatch.fnmatch(p.name, g) for g in include_globs):
                yield p


def _cap_copy(files: list[Path], dest: Path, max_total_bytes: int) -> tuple[int, int]:
    total = 0
    copied = 0
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        size = f.stat().st_size
        if total + size > max_total_bytes:
            continue
        rel = re.sub(r"[:\\\\/]+", "_", str(f))
        target = dest / rel
        try:
            shutil.copy2(f, target)
            total += size
            copied += 1
        except OSError:
            continue
    return copied, total


def collect_logs_step(config: Config, run_dir: Path, params: dict[str, Any]) -> dict[str, Any]:
    logs_cfg = config.get("logs", {})
    roots = [str(r) for r in (logs_cfg.get("roots", []) or [])]
    include_globs = [str(g) for g in (logs_cfg.get("include_globs", ["*.log"]) or ["*.log"])]
    max_total_mb = int(logs_cfg.get("max_total_mb", 50))
    max_total_bytes = max_total_mb * 1024 * 1024

    files = sorted(set(_iter_files(roots, include_globs)))
    dest = run_dir / "artifacts" / "logs"
    copied, total_bytes = _cap_copy(files, dest, max_total_bytes)

    return {
        "ok": True,
        "roots": roots,
        "matched": len(files),
        "copied": copied,
        "total_mb": round(total_bytes / (1024 * 1024), 2),
        "dest": str(dest),
    }


def scan_crash_step(config: Config, run_dir: Path, params: dict[str, Any]) -> dict[str, Any]:
    sig = config.get("crash_signatures", {})
    strings = [str(s) for s in (sig.get("strings", []) or [])]
    file_globs = [str(g) for g in (sig.get("file_globs", []) or [])]

    log_dir = run_dir / "artifacts" / "logs"
    if not log_dir.exists():
        return {"ok": False, "reason": "no collected logs found", "log_dir": str(log_dir)}

    hits: list[dict[str, Any]] = []
    crash_files: list[str] = []

    for p in log_dir.rglob("*"):
        if not p.is_file():
            continue
        if any(fnmatch.fnmatch(p.name, g) for g in file_globs):
            crash_files.append(str(p))

        # Only scan text-like files.
        if not any(p.name.lower().endswith(ext) for ext in (".log", ".txt", ".json")):
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for s in strings:
            if s and s in content:
                hits.append({"file": str(p), "signature": s})

    ok = (len(hits) == 0) and (len(crash_files) == 0)
    return {
        "ok": ok,
        "signature_hits": hits[:200],
        "crash_files": crash_files[:200],
        "note": "ok=false when crash signatures or dump-like files are detected",
    }


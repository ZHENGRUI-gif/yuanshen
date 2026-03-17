from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any

from hsrqa.core.config import Config


def ahk_run_script_step(config: Config, run_dir: Path, params: dict[str, Any]) -> dict[str, Any]:
    """
    Runs an AutoHotkey script to drive UI flows on Windows.

    Required config:
    - pc.ahk_exe: path to AutoHotkey executable (e.g., AutoHotkey64.exe)

    Params:
    - script: path to .ahk file (repo-relative or absolute)
    - timeout_sec: max run time
    - args: list of extra args passed to the script
    """
    pc = config.get("pc", {})
    ahk_exe = pc.get("ahk_exe")
    script = params.get("script")
    timeout_sec = int(params.get("timeout_sec", 300))
    args = params.get("args", []) or []

    if not ahk_exe:
        return {"ok": False, "reason": "pc.ahk_exe is not set (AutoHotkey not configured)"}
    if not script:
        return {"ok": False, "reason": "params.script is required"}

    ahk_path = Path(str(ahk_exe))
    if not ahk_path.exists():
        return {"ok": False, "reason": "ahk_exe not found", "ahk_exe": str(ahk_path)}

    script_path = Path(str(script))
    if not script_path.is_absolute():
        # Resolve repo-relative scripts (usually under qa/flows).
        script_path = Path.cwd() / script_path
    if not script_path.exists():
        return {"ok": False, "reason": "script not found", "script": str(script_path)}

    stdout_path = run_dir / f"ahk_{script_path.stem}_stdout.txt"
    stderr_path = run_dir / f"ahk_{script_path.stem}_stderr.txt"

    started = time.time()
    with stdout_path.open("wb") as out, stderr_path.open("wb") as err:
        proc = subprocess.Popen(  # noqa: S603,S607 - intentional external process launch
            [str(ahk_path), str(script_path), *[str(a) for a in args]],
            cwd=str(script_path.parent),
            stdout=out,
            stderr=err,
        )
        try:
            proc.wait(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
            return {
                "ok": False,
                "reason": "ahk script timeout",
                "timeout_sec": timeout_sec,
                "stdout": str(stdout_path),
                "stderr": str(stderr_path),
            }

    duration = round(time.time() - started, 2)
    ok = proc.returncode == 0
    return {
        "ok": ok,
        "exit_code": proc.returncode,
        "duration_sec": duration,
        "script": str(script_path),
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
    }


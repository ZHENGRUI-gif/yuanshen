from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any

from hsrqa.core.config import Config


def launch_and_idle_step(config: Config, run_dir: Path, params: dict[str, Any]) -> dict[str, Any]:
    pc = config.get("pc", {})
    game_exe = pc.get("game_exe")
    working_dir = pc.get("working_dir")
    args = pc.get("args", []) or []
    startup_timeout_sec = int(pc.get("startup_timeout_sec", 60))
    kill_timeout_sec = int(pc.get("kill_timeout_sec", 10))

    runtime_sec = int(params.get("runtime_sec", pc.get("runtime_smoke_sec", 120)))

    if not game_exe:
        return {"ok": False, "reason": "pc.game_exe is not set"}

    exe_path = Path(game_exe)
    if not exe_path.exists():
        return {"ok": False, "reason": "game_exe not found", "game_exe": str(exe_path)}

    cwd = Path(working_dir) if working_dir else exe_path.parent
    if not cwd.exists():
        return {"ok": False, "reason": "working_dir not found", "working_dir": str(cwd)}

    stdout_path = run_dir / "pc_stdout.txt"
    stderr_path = run_dir / "pc_stderr.txt"

    started = time.time()
    with stdout_path.open("wb") as out, stderr_path.open("wb") as err:
        proc = subprocess.Popen(  # noqa: S603,S607 - intentional external process launch
            [str(exe_path), *[str(a) for a in args]],
            cwd=str(cwd),
            stdout=out,
            stderr=err,
        )

        # Basic liveness check during startup window.
        deadline = time.time() + startup_timeout_sec
        while time.time() < deadline:
            if proc.poll() is not None:
                return {
                    "ok": False,
                    "reason": "process exited during startup",
                    "exit_code": proc.returncode,
                    "stdout": str(stdout_path),
                    "stderr": str(stderr_path),
                }
            time.sleep(1)

        # Idle runtime window.
        time.sleep(max(0, runtime_sec))

        # Attempt graceful termination first.
        proc.terminate()
        try:
            proc.wait(timeout=kill_timeout_sec)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=kill_timeout_sec)

    duration = round(time.time() - started, 2)
    return {
        "ok": True,
        "duration_sec": duration,
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
        "exit_code": proc.returncode,
    }


from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from hsrqa.core.config import Config


def toggle_interface_step(config: Config, run_dir: Path, params: dict[str, Any]) -> dict[str, Any]:
    """
    Disruptive: toggles a Windows network interface (disable/enable).

    Guard rails:
    - Requires config.network.allow_disruptive == true

    Params:
    - name: interface name (e.g., "WLAN", "Ethernet")
    - state: "disable" or "enable"
    """
    net_cfg = config.get("network", {}) or {}
    if not bool(net_cfg.get("allow_disruptive", False)):
        return {"ok": False, "reason": "network.allow_disruptive is false (refusing disruptive action)"}

    name = params.get("name")
    state = params.get("state")
    if not name or state not in ("disable", "enable"):
        return {"ok": False, "reason": "params.name and params.state(disable|enable) are required"}

    admin = "disabled" if state == "disable" else "enabled"
    cmd = ["netsh", "interface", "set", "interface", f"name={name}", f"admin={admin}"]

    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=30)  # noqa: S603
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "reason": "failed to run netsh", "error": repr(e), "cmd": cmd}

    ok = cp.returncode == 0
    return {
        "ok": ok,
        "cmd": cmd,
        "returncode": cp.returncode,
        "stdout": (cp.stdout or "").strip(),
        "stderr": (cp.stderr or "").strip(),
        "note": "May require elevated privileges; if it fails, run terminal as admin or use an approved network tool.",
    }


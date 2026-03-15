from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from hsrqa.core.config import Config
from hsrqa.core.report import StepResult, SuiteResult, write_html, write_json
from hsrqa.steps.logs import collect_logs_step, scan_crash_step
from hsrqa.steps.pc import launch_and_idle_step


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Runner:
    def __init__(self, config: Config, out_root: Path) -> None:
        self.config = config
        self.out_root = out_root

        self.step_registry: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
            "pc.launch_and_idle": self._wrap(launch_and_idle_step),
            "logs.collect": self._wrap(collect_logs_step),
            "logs.scan_crash": self._wrap(scan_crash_step),
        }

    def _wrap(self, fn: Callable[[Config, Path, dict[str, Any]], dict[str, Any]]):
        def runner(params: dict[str, Any]) -> dict[str, Any]:
            return fn(self.config, self._run_dir, params)

        return runner

    def _load_suite(self, suite_id: str) -> dict[str, Any]:
        suite_path = Path("qa/suites") / f"{suite_id}.json"
        if not suite_path.exists():
            raise FileNotFoundError(f"Suite not found: {suite_path}")
        return json.loads(suite_path.read_text(encoding="utf-8"))

    def run_suite(self, suite_id: str) -> int:
        suite = self._load_suite(suite_id)
        suite_name = suite.get("name", suite_id)
        started_at = _now_iso()

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._run_dir = self.out_root / ts
        self._run_dir.mkdir(parents=True, exist_ok=True)

        # Keep a stable path for the latest run (directory copy after results are produced).
        latest = self.out_root / "latest"

        steps: list[StepResult] = []
        ok = True

        for step in suite.get("steps", []):
            step_id = step.get("id", "step")
            step_type = step.get("type")
            params = step.get("params", {}) or {}

            s_started = _now_iso()
            details: dict[str, Any] = {}
            s_ok = False

            try:
                if step_type not in self.step_registry:
                    raise KeyError(f"Unknown step type: {step_type}")
                details = self.step_registry[step_type](params)
                s_ok = bool(details.get("ok", True))
            except Exception as e:  # noqa: BLE001 - runner must not crash
                s_ok = False
                details = {
                    "ok": False,
                    "error": repr(e),
                }

            s_finished = _now_iso()
            steps.append(
                StepResult(
                    id=step_id,
                    type=step_type,
                    ok=s_ok,
                    started_at=s_started,
                    finished_at=s_finished,
                    details=details,
                )
            )

            if not s_ok:
                ok = False

        finished_at = _now_iso()
        artifacts = {
            "run_dir": str(self._run_dir),
        }

        result = SuiteResult(
            suite_id=suite_id,
            suite_name=suite_name,
            ok=ok,
            started_at=started_at,
            finished_at=finished_at,
            steps=steps,
            artifacts=artifacts,
        )

        json_path = self._run_dir / "result.json"
        html_path = self._run_dir / "report.html"
        write_json(result, json_path)
        write_html(result, html_path)

        # Refresh latest copy with populated artifacts.
        if latest.exists():
            shutil.rmtree(latest)
        shutil.copytree(self._run_dir, latest)

        return 0 if ok else 2

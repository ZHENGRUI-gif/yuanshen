from __future__ import annotations

import html
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class StepResult:
    id: str
    type: str
    ok: bool
    started_at: str
    finished_at: str
    details: dict[str, Any]


@dataclass
class SuiteResult:
    suite_id: str
    suite_name: str
    ok: bool
    started_at: str
    finished_at: str
    steps: list[StepResult]
    artifacts: dict[str, str]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(result: SuiteResult, path: Path) -> None:
    payload = {
        "suite_id": result.suite_id,
        "suite_name": result.suite_name,
        "ok": result.ok,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
        "artifacts": result.artifacts,
        "steps": [
            {
                "id": s.id,
                "type": s.type,
                "ok": s.ok,
                "started_at": s.started_at,
                "finished_at": s.finished_at,
                "details": s.details,
            }
            for s in result.steps
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_html(result: SuiteResult, path: Path) -> None:
    def esc(x: Any) -> str:
        return html.escape(str(x))

    rows = []
    for s in result.steps:
        status = "PASS" if s.ok else "FAIL"
        rows.append(
            "<tr>"
            f"<td>{esc(s.id)}</td>"
            f"<td>{esc(s.type)}</td>"
            f"<td class='{status.lower()}'>{esc(status)}</td>"
            f"<td><pre>{esc(json.dumps(s.details, ensure_ascii=False, indent=2))}</pre></td>"
            "</tr>"
        )

    artifact_rows = []
    for k, v in result.artifacts.items():
        artifact_rows.append(f"<li><b>{esc(k)}:</b> {esc(v)}</li>")

    ok_text = "PASS" if result.ok else "FAIL"
    started = esc(result.started_at)
    finished = esc(result.finished_at)
    suite_name = esc(result.suite_name)

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>QA Report - {suite_name}</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 24px; }}
    .header {{ display: flex; gap: 16px; align-items: baseline; flex-wrap: wrap; }}
    .badge {{ padding: 4px 10px; border-radius: 999px; color: white; font-weight: 700; }}
    .pass {{ background: #177245; }}
    .fail {{ background: #b00020; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 16px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; vertical-align: top; }}
    th {{ background: #f6f6f6; text-align: left; }}
    td pre {{ margin: 0; white-space: pre-wrap; word-break: break-word; }}
    .hint {{ color: #666; }}
    .pass, .fail {{ color: white; }}
    td.pass, td.fail {{ font-weight: 700; text-align: center; }}
  </style>
</head>
<body>
  <div class="header">
    <h1 style="margin:0;">QA Report</h1>
    <span class="badge {'pass' if result.ok else 'fail'}">{ok_text}</span>
    <div class="hint">Started: {started} | Finished: {finished}</div>
  </div>
  <h2 style="margin-top:16px;">Suite</h2>
  <div><b>ID:</b> {esc(result.suite_id)}</div>
  <div><b>Name:</b> {suite_name}</div>
  <h2 style="margin-top:16px;">Artifacts</h2>
  <ul>
    {''.join(artifact_rows) if artifact_rows else '<li class="hint">None</li>'}
  </ul>
  <h2 style="margin-top:16px;">Steps</h2>
  <table>
    <thead><tr><th>Step</th><th>Type</th><th>Status</th><th>Details</th></tr></thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""
    path.write_text(html_doc, encoding="utf-8")


__all__ = ["StepResult", "SuiteResult", "write_json", "write_html", "_now_iso"]


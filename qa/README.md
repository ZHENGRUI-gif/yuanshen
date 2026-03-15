# HSR QA Automation (Skeleton)

This folder contains a lightweight, dependency-free (stdlib-only) automation harness intended for end-to-end sanity/smoke/regression checks of a game client like Honkai: Star Rail.

What it can do without extra tooling:
- Start/stop the game process (PC Windows).
- Capture basic runtime signals (exit code, runtime duration).
- Collect logs and scan for crash signatures.
- Run suites (smoke/regression) defined in JSON.
- Produce a simple HTML report.

What it is designed to plug into later:
- ADB/Appium (Android/iOS) device control.
- Network shaping (weak network, packet loss) via external tooling.
- Crash dump symbolication, perf tracing, and telemetry ingestion.

## Quick Start

1) Create a config:
- Copy `qa/config.example.json` to `qa/config.json` and fill paths.

2) Run a suite:
```powershell
python qa/run.py --config qa/config.json --suite smoke
```

3) View report:
- `qa/out/latest/report.html`

## Notes
- The harness is intentionally conservative: it will not run destructive system commands (e.g., changing firewall rules).
- For mobile automation, implement `qa/hsrqa/adapters/adb_adapter.py` and `qa/hsrqa/adapters/appium_adapter.py` and wire them into suites.


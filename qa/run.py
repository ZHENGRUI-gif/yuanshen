from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from hsrqa.core.config import load_config
from hsrqa.core.runner import Runner


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="HSR QA automation runner (stdlib-only).")
    parser.add_argument("--config", required=True, help="Path to config JSON (e.g., qa/config.json)")
    parser.add_argument("--suite", required=True, help="Suite id (e.g., smoke, regression)")
    parser.add_argument("--out", default="qa/out", help="Output directory (default: qa/out)")
    args = parser.parse_args(argv)

    config_path = Path(args.config)
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    config = load_config(config_path)
    runner = Runner(config=config, out_root=out_root)
    return runner.run_suite(args.suite)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


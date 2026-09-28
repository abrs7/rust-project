#!/usr/bin/env python3
"""Adversarial candidates for telemetry-array-rebuild verifier checks."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fragments")
    parser.add_argument("--campaigns")
    parser.add_argument("--references")
    parser.add_argument("--output")
    parser.add_argument(
        "--mode",
        choices=("nop", "reject", "constant", "tamper"),
        default="nop",
    )
    args = parser.parse_args()
    if args.mode == "reject":
        return 2
    if args.mode == "tamper":
        try:
            Path("/logs/verifier/reward.txt").write_text("1\n", encoding="utf-8")
        except OSError:
            pass
    # nop and constant intentionally do not reconstruct hidden inputs.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

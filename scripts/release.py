#!/usr/bin/env python3
"""Release procedure wrapper. Dry-run only until publication credentials exist."""
from __future__ import annotations

import argparse, sys

from meshanvil import VERSION

MEASURED = [
    "macOS: Blender 5.2, host Python 3.11.15, FreeCAD 1.0",
    "Windows: Blender 5.2 installed, host Python 3.10.4",
    "WSL Ubuntu: host Python 3.14.4, Windows Blender reachable through /mnt/c",
    "Linux: unverified; no Blender-equipped Linux machine measured",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="print the release facts and publish nothing")
    args = parser.parse_args(argv)
    if not args.dry_run:
        print("release publishing is not configured; run with --dry-run", file=sys.stderr)
        return 2
    print(f"meshanvil {VERSION} release dry run")
    print("channel: Python package index")
    print("publishes: nothing")
    for line in MEASURED:
        print(f"- {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Fail a built wheel that forgot a runtime asset."""
from __future__ import annotations

import json, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = [
    "meshanvil/__init__.py",
    "meshanvil/cli.py",
    "meshanvil_engine/report.py",
    "locales/en.json",
    "locales/fr.json",
    "viewer/index.html",
    "viewer/viewer.css",
    "viewer/viewer.js",
    "viewer/icon.png",
    "viewer/src/app.js",
    "viewer/src/live.js",
    "viewer/src/markdown.js",
]


def expected() -> list[str]:
    files = [*STATIC]
    for manifest in sorted((ROOT / "tools").glob("*.op.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        files.append(f"tools/{manifest.name}")
        files.append(data["script"])
    for script in sorted((ROOT / "pipeline").glob("*.py")):
        files.append(f"pipeline/{script.name}")
    return sorted(set(files))


def main(argv: list[str]) -> int:
    wheels = [Path(arg) for arg in argv]
    if len(wheels) != 1 or not wheels[0].is_file():
        print("usage: check_package.py dist/meshanvil-*.whl", file=sys.stderr)
        return 2
    with zipfile.ZipFile(wheels[0]) as wheel:
        names = set(wheel.namelist())
        metadata = next(name for name in names if name.endswith(".dist-info/METADATA"))
        entry_points = next(name for name in names if name.endswith(".dist-info/entry_points.txt"))
        metadata_text = wheel.read(metadata).decode("utf-8")
        entry_text = wheel.read(entry_points).decode("utf-8")
    missing = [name for name in expected() if name not in names]
    if missing:
        for name in missing:
            print(f"package missing asset: {name}", file=sys.stderr)
        return 1
    if "Requires-Dist:" in metadata_text:
        print("package declares a runtime dependency", file=sys.stderr)
        return 1
    if "meshanvil = meshanvil.cli:main" not in entry_text:
        print("package missing meshanvil console script", file=sys.stderr)
        return 1
    print(f"package assets: ok ({len(expected())} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

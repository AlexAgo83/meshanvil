"""Explicit lifecycle changes for report-owned artefacts."""
from __future__ import annotations
import json, time
from pathlib import Path

OPS = "work/ops"


def candidates(root: Path, keep: int) -> list[tuple[Path, dict, Path]]:
    grouped: dict[str, list[tuple[Path, dict, Path]]] = {}
    project = root.resolve()
    source = (root / "work" / "in").resolve()
    for report_path in sorted((root / OPS).glob("*.json")):
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            output = report.get("output") or {}
            path = Path(output["path"]).resolve()
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            continue
        if output.get("state") != "present" or path == source or source in path.parents:
            continue
        if path != project and project not in path.parents:
            continue
        if output.get("pinned") or report.get("links", {}).get("docs"):
            continue
        grouped.setdefault(report.get("chain") or report.get("id"), []).append((report_path, report, path))
    return [item for values in grouped.values() for item in (values if keep == 0 else values[:-keep])
            if item[2].is_file()]


def run(root: Path, keep: int, dry_run: bool) -> tuple[list[tuple[Path, int]], int]:
    selected = candidates(root, keep)
    result = [(path, path.stat().st_size) for _, _, path in selected]
    if dry_run:
        return result, sum(size for _, size in result)
    for report_path, report, path in selected:
        size = path.stat().st_size
        path.unlink()
        report["output"]["state"] = "pruned"
        report["output"]["state_changed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        report_path.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return result, sum(size for _, size in result)

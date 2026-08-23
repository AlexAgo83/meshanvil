"""Small report index for CLI callers that should not walk work/ops themselves."""
from __future__ import annotations
import json
from pathlib import Path

from . import runner


def files(root: Path) -> list[Path]:
    return sorted((root / runner.OPS).glob("*.json"))


def _rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load(path: Path) -> tuple[dict | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as error:
        return None, f"malformed_json:{error.lineno}:{error.colno}"
    except OSError as error:
        return None, f"unreadable:{error}"


def summary(root: Path, path: Path) -> dict:
    report, warning = load(path)
    item = {"id": path.name.split("_", 1)[0], "path": _rel(root, path)}
    if warning:
        return {**item, "warning": {"code": "malformed_report", "message": warning}}
    output = report.get("output") or {}
    source = report.get("input") or {}
    item.update({
        "id": report.get("id") or item["id"],
        "operation": report.get("operation"),
        "status": report.get("status"),
        "input_path": source.get("path") or report.get("target"),
        "output_path": output.get("path"),
        "output_state": output.get("state"),
        "created_at": report.get("created_at") or report.get("started_at") or report.get("finished_at"),
    })
    return {key: value for key, value in item.items() if value is not None}


def list_reports(root: Path) -> list[dict]:
    return [summary(root, path) for path in files(root)]


def latest(root: Path) -> Path | None:
    """The most recently written report, which is not the last name in the chain.

    `--from` allocates a sibling on its parent's ordinal, so branching off 001 after 005
    exists writes 002a -- a name that sorts before the five reports preceding it. Listing
    stays in chain order; only "latest" means time, and the filesystem already knows it.
    """
    found = files(root)
    return max(found, key=lambda path: (path.stat().st_mtime_ns, path.name), default=None)


def find(root: Path, identity: str) -> tuple[Path | None, str | None]:
    matches = []
    for path in files(root):
        report, _warning = load(path)
        report_id = (report or {}).get("id") or path.name.split("_", 1)[0]
        if report_id == identity:
            return path, None
        if report_id.startswith(identity):
            matches.append(path)
    if len(matches) == 1:
        return matches[0], None
    if matches:
        return None, "ambiguous_report_id"
    return None, "report_not_found"

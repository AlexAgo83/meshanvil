"""Read-only project state for agents."""
from __future__ import annotations
import os, shutil
from pathlib import Path

from . import engines, manifests, paths, reports, runner
from .i18n import t


def _engine(name: str, required: bool) -> dict:
    item = {"name": name, "class": "required" if required else "optional", "required": required,
            "override": engines.OVERRIDE[name],
            "minimum_version": ".".join(map(str, engines.MIN_VERSION[name]))}
    try:
        found = engines.find(name)
    except engines.EngineMissing:
        item.update(state="missing", path=None, version=None)
    else:
        item.update(state="found", path=str(found), version=None)
    item["reason"] = t(f"doctor.{name}.reason")
    item["fix"] = engines.fix_command(name)
    return item


def _work(root: Path) -> dict:
    path = root / "work"
    state = "found" if path.is_dir() and os.access(path, os.W_OK) else "missing"
    return {"name": "work", "class": "required", "required": True, "state": state,
            "path": str(path), "free_bytes": shutil.disk_usage(path).free if path.is_dir() else 0,
            "reason": t("doctor.work.reason"), "fix": "mkdir work" if os.name == "nt" else "mkdir -p work"}


def collect() -> dict:
    root, rule = paths.resolve()
    requirements = [_engine("blender", True), _engine("freecad", False), _work(root)]
    blocker = next((item["name"] for item in requirements if item["required"] and item["state"] != "found"), None)
    ops = manifests.discover()
    summaries = reports.list_reports(root)
    latest = summaries[-1] if summaries else None
    data = {
        "ok": blocker is None,
        "project": {"name": paths.name(root), "path": str(root), "resolved_by": rule,
                    "marker": (root / paths.MARKER).is_dir()},
        "doctor": {"ok": blocker is None, "next": blocker, "requirements": requirements},
        "operations": {"count": len(ops), "names": sorted(ops)},
        "reports": {"count": len(summaries), "latest": latest},
        "viewer": {"useful": bool(summaries), "command": "meshanvil view"},
    }
    data["next"] = next_actions(data)
    return data


def next_actions(data: dict) -> list[dict]:
    actions = []
    if not data["project"]["marker"]:
        actions.append({"reason": "no_project_marker", "command": "meshanvil init ."})
    if not data["doctor"]["ok"]:
        blocker = data["doctor"]["next"]
        requirement = next(item for item in data["doctor"]["requirements"] if item["name"] == blocker)
        actions.append({"reason": f"{blocker}_missing", "command": requirement["fix"]})
    if data["operations"]["count"] == 0:
        actions.append({"reason": "no_operations_found", "command": "meshanvil list --json"})
    if data["reports"]["count"] == 0:
        actions.append({"reason": "no_reports_yet", "command": "meshanvil demo"})
    else:
        actions.append({"reason": "reports_present", "command": "meshanvil reports --latest --json"})
        actions.append({"reason": "viewer_useful", "command": "meshanvil view"})
    return actions

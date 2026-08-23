"""Read-only project state for agents."""
from __future__ import annotations

from . import doctor, manifests, paths, reports


def collect() -> dict:
    """One preflight answer, built from the same setup inspection `doctor` reports.

    Read-only: `inspect(write=False)` is the whole reason this does not simply call `check`,
    which writes work/doctor.json. Reusing it is also what keeps the engine versions here --
    a requirement that states a minimum and no actual version cannot be checked against it.
    """
    root, rule = paths.resolve()
    setup = doctor.inspect(root, write=False)
    ops = manifests.discover()
    summaries = reports.list_reports(root)
    newest = reports.latest(root)                 # by time, not by name: see reports.latest
    data = {
        "ok": setup["ok"],
        "project": {"name": paths.name(root), "path": str(root), "resolved_by": rule,
                    "marker": (root / paths.MARKER).is_dir()},
        "doctor": {"ok": setup["ok"], "next": setup["next"],
                   "requirements": setup["requirements"]},
        "operations": {"count": len(ops), "names": sorted(ops)},
        "reports": {"count": len(summaries),
                    "latest": reports.summary(root, newest) if newest else None},
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
        actions.append({"reason": doctor.blocker_code(blocker), "command": requirement["fix"]})
    if data["operations"]["count"] == 0:
        actions.append({"reason": "no_operations_found", "command": "meshanvil list --json"})
    if data["reports"]["count"] == 0:
        actions.append({"reason": "no_reports_yet", "command": "meshanvil demo"})
    else:
        actions.append({"reason": "reports_present", "command": "meshanvil reports --latest --json"})
        actions.append({"reason": "viewer_useful", "command": "meshanvil view"})
    return actions

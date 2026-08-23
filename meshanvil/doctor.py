"""Inspect the local setup without installing or changing anything."""
from __future__ import annotations
import json, os, shutil
from pathlib import Path

from . import engines, paths
from .i18n import t

CACHE = "work/.doctor-cache.json"
REPORT = "work/doctor.json"
CACHE_VERSION = 2


def _reason(name: str) -> str:
    return {"blender": t("doctor.blender.reason"), "freecad": t("doctor.freecad.reason"),
            "work": t("doctor.work.reason")}[name]


def _engine(name: str, required: bool) -> dict:
    item = {"name": name, "class": "required" if required else "optional", "required": required,
            "override": engines.OVERRIDE[name],
            "minimum_version": ".".join(map(str, engines.MIN_VERSION[name]))}
    try:
        path = engines.find(name)
    except engines.EngineMissing:
        item.update(state="missing", path=None, version=None)
    else:
        number, _build = engines.version(path)
        item.update(state="too_old" if number and not engines.meets_floor(name, number) else "found",
                    path=str(path), version=number or None, mtime_ns=path.stat().st_mtime_ns)
    item["reason"] = _reason(name)
    item["fix"] = engines.fix_command(name)
    return item


def work(root: Path) -> dict:
    path = root / "work"
    if not path.is_dir():
        state = "missing"
    else:
        try:
            probe = path / f".doctor-write-{os.getpid()}"
            probe.write_text("", encoding="utf-8")
            probe.unlink()
            state = "found"
        except OSError:
            state = "missing"
    return {"name": "work", "class": "required", "required": True, "state": state, "path": str(path),
            "free_bytes": shutil.disk_usage(path).free if path.is_dir() else 0,
            "reason": t("doctor.work.reason"),
            "fix": "mkdir work" if os.name == "nt" else "mkdir -p work"}


def _write_if_work_exists(path: Path, data: dict) -> None:
    if path.parent.is_dir():
        path.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")


def _engine_signature() -> list[dict]:
    items = []
    for name in ("blender", "freecad"):
        try:
            path = engines.find(name)
        except engines.EngineMissing:
            items.append({"name": name, "path": None, "mtime_ns": None})
        else:
            items.append({"name": name, "path": str(path), "mtime_ns": path.stat().st_mtime_ns})
    return items


def blocker_code(name: str | None) -> str:
    """The stable error code for a failing requirement.

    One place, because `doctor --json` and `status --json` answer the same question and an
    agent branches on the identifier: two spellings of one condition is two conditions.
    """
    return {"blender": "engine_missing", "freecad": "engine_missing",
            "work": "work_unavailable"}.get(name, "setup_refused")


def inspect(root: Path, write: bool = True) -> dict:
    """Collect the setup result. `write` is what separates a check from a report."""
    signature = _engine_signature()
    cache_path = root / CACHE
    try:
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        cached = {}
    if cached.get("schema_version") == CACHE_VERSION and cached.get("signature") == signature:
        current = cached["engines"]
    else:
        current = [_engine("blender", True), _engine("freecad", False)]
        if write:
            _write_if_work_exists(cache_path, {"schema_version": CACHE_VERSION,
                                               "signature": signature, "engines": current})
    for item in current:
        item["reason"] = _reason(item["name"])
    requirements = [*current, work(root)]
    blocker = next((item["name"] for item in requirements if item["required"] and item["state"] != "found"), None)
    active, rule = paths.resolve()
    # An operator has to be able to see where a destructive run will land, and the working
    # directory only tells them that if the tool says what it made of it.
    result = {"ok": blocker is None, "next": blocker, "requirements": requirements,
              "project": {"name": paths.name(active), "path": str(active), "resolved_by": rule}}
    if write:
        _write_if_work_exists(root / REPORT, result)
    return result


def check(root: Path) -> dict:
    """Write one machine-readable setup result when work/ exists; otherwise report only."""
    return inspect(root, write=True)

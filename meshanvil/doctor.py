"""Inspect the local setup without installing or changing anything."""
from __future__ import annotations
import json, os, shutil
from pathlib import Path

from . import engines
from .i18n import t

CACHE = "work/.doctor-cache.json"
REPORT = "work/doctor.json"
CACHE_VERSION = 1


def _reason(name: str) -> str:
    return {"blender": t("doctor.blender.reason"), "freecad": t("doctor.freecad.reason"),
            "work": t("doctor.work.reason")}[name]


def _engine(name: str, required: bool) -> dict:
    item = {"name": name, "required": required, "override": engines.OVERRIDE[name],
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


def _work(root: Path) -> dict:
    path = root / "work"
    try:
        path.mkdir(exist_ok=True)
        probe = path / f".doctor-write-{os.getpid()}"
        probe.write_text("", encoding="utf-8")
        probe.unlink()
        state = "found"
    except OSError:
        state = "missing"
    return {"name": "work", "required": True, "state": state, "path": str(path),
            "free_bytes": shutil.disk_usage(path).free if path.exists() else 0,
            "reason": t("doctor.work.reason"), "fix": "mkdir -p work"}


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


def check(root: Path) -> dict:
    """Write one machine-readable setup result; engine probes are cached while binaries stay put."""
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
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({"schema_version": CACHE_VERSION, "signature": signature,
                                          "engines": current}, indent=1) + "\n",
                              encoding="utf-8")
    for item in current:
        item["reason"] = _reason(item["name"])
    requirements = [*current, _work(root)]
    blocker = next((item["name"] for item in requirements if item["required"] and item["state"] != "found"), None)
    result = {"ok": blocker is None, "next": blocker, "requirements": requirements}
    report_path = root / REPORT
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    return result

"""An operation is a script plus a manifest sitting next to it, named <script>.op.json."""
from __future__ import annotations
import json
from pathlib import Path

from .i18n import t

SEARCH = ("tools", "pipeline")


def root() -> Path:
    return Path(__file__).resolve().parent.parent


def discover() -> dict[str, dict]:
    """Every manifest found, keyed by operation name. Adding a script adds an operation."""
    found: dict[str, dict] = {}
    for directory in SEARCH:
        for path in sorted((root() / directory).glob("*.op.json")):
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["manifest_path"] = str(path.relative_to(root()))
            found[manifest["operation"]] = manifest
    return found


def resolve(manifest: dict, given: dict[str, str]) -> dict:
    """Command-line values over declared defaults, converted to the declared type."""
    casts = {"int": int, "float": float, "str": str,
             "bool": lambda v: str(v).lower() in ("1", "true", "yes", "on")}
    values: dict[str, object] = {}
    for spec in manifest.get("params", []):
        name = spec["name"]
        raw = given.get(name)
        values[name] = spec.get("default") if raw is None else casts[spec["type"]](raw)
    unknown = set(given) - {spec["name"] for spec in manifest.get("params", [])}
    if unknown:
        raise KeyError(t("run.unknown_parameters", names=", ".join(sorted(unknown))))
    return values

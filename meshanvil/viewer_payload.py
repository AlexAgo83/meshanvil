"""Build the viewer files and data payload."""
from __future__ import annotations

import json, os, shutil, time
from pathlib import Path

from . import VERSION, logics_bridge, paths
from .i18n import SOURCE, catalogue, language

OPS = "work/ops"
OUT = "work/viewer"


def collect(root: Path, page: Path) -> list[dict]:
    reports = []
    for path in sorted((root / OPS).glob("*.json")):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if report.get("id"):
            reports.append(with_render_urls(page, report))
    reports.sort(key=lambda r: (r["id"].rstrip("abcdefghijklmnopqrstuvwxyz"), r["id"]))
    return reports


def with_render_urls(page: Path, report: dict) -> dict:
    for render in report.get("renders", []):
        try:
            render["url"] = os.path.relpath(render["path"], page)
        except ValueError:
            render["url"] = render["path"]
    for pair in report.get("comparisons", []):
        for state in ("before", "after"):
            try:
                pair[f"{state}_url"] = os.path.relpath(pair[state], page)
            except ValueError:
                pair[f"{state}_url"] = pair[state]
    return report


def collect_doctor(root: Path) -> dict | None:
    try:
        value = json.loads((root / "work" / "doctor.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def payload(root: Path, target: Path, run_token: str | None = None) -> dict:
    strings = {**catalogue(SOURCE), **catalogue(language())}
    catalogs = {code.stem: catalogue(code.stem) for code in sorted((paths.code_root() / "locales").glob("*.json"))}
    known = [{"name": paths.name(project), "path": str(project),
              "reports": collect(project, target),
              "ops_exists": (project / OPS).is_dir()}
             for project in paths.projects(root)]
    active = next((entry for entry in known if entry["reports"]), known[0])
    runbooks = logics_bridge.runbooks(paths.code_root())
    refs = {ref for entry in known for report in entry["reports"]
            for ref in report.get("links", {}).get("docs", [])}
    refs |= {doc["ref"] for doc in runbooks}
    return {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "root": str(root), "lang": language(), "strings": strings, "catalogs": catalogs,
            "version": VERSION, "run_token": run_token, "projects": known, "active": active["name"],
            "reports": active["reports"], "docs": logics_bridge.documents(refs),
            "runbooks": runbooks, "doctor": collect_doctor(root),
            "ops_exists": active["ops_exists"]}


def build(root: Path, run_token: str | None = None) -> tuple[Path, dict]:
    target = root / OUT
    target.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "viewer.css", "viewer.js", "icon.png"):
        shutil.copyfile(paths.code_root() / "viewer" / name, target / name)
    data = payload(root, target, run_token)
    (target / "data.js").write_text(
        "window.MESHANVIL = " + json.dumps(data, indent=1) + ";\n", encoding="utf-8")
    return target / "index.html", data

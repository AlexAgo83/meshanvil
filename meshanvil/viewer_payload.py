"""Build the viewer files and data payload."""
from __future__ import annotations

import hashlib, json, os, shutil, time
from pathlib import Path, PureWindowsPath

from . import VERSION, logics_bridge, notes, paths
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


def _url(target: str, page: Path) -> str:
    """A relative URL, which on Windows is not what `relpath` returns.

    `relpath` answers in the host's separator, so a page written on Windows carried
    `..\\renders\\001_3q.png` into an `img src`. Chromium happens to fold a backslash into a
    slash for file:, so it loaded anyway -- on leniency, not on a correct URL. Say it properly.
    """
    try:
        # PureWindowsPath parses both separators on any host, which is what makes this
        # check-able from macOS: the bug only exists where relpath answers in backslashes.
        return PureWindowsPath(os.path.relpath(target, page)).as_posix()
    except ValueError:
        return target


def with_render_urls(page: Path, report: dict) -> dict:
    for render in report.get("renders", []):
        render["url"] = _url(render["path"], page)
    for pair in report.get("comparisons", []):
        for state in ("before", "after"):
            pair[f"{state}_url"] = _url(pair[state], page)
    return report


def collect_doctor(root: Path) -> dict | None:
    try:
        value = json.loads((root / "work" / "doctor.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def payload(root: Path, target: Path, run_token: str | None = None, full: bool = True) -> dict:
    """The page's data. `full` carries everything; the served first paint does not.

    A first paint that ships every sibling project's reports and every runbook's body pays for
    all of it before anything is clicked -- measured at 623 KB, of which 217 KB was projects
    nobody had selected and 124 KB documents nobody had opened. The snapshot written for a page
    opened from the filesystem stays full, because it has no server to ask afterwards.

    `files` is always complete: it is the map the file controls resolve an id through, and a
    project's reports can arrive later while their files cannot."""
    strings = {**catalogue(SOURCE), **catalogue(language())}
    catalogs = {code.stem: catalogue(code.stem) for code in sorted(paths.asset_root("locales").glob("*.json"))}
    known = [{"name": paths.name(project), "path": str(project),
              "reports": collect(project, target),
              "ops_exists": (project / OPS).is_dir()}
             for project in paths.projects(root)]
    active = next((entry for entry in known if entry["reports"]), known[0])
    runbooks = logics_bridge.runbooks(root)
    refs = {ref for entry in known for report in entry["reports"]
            for ref in report.get("links", {}).get("docs", [])}
    refs |= {doc["ref"] for doc in runbooks}
    projects = known if full else [
        {**entry, "reports": entry["reports"] if entry["name"] == active["name"] else []}
        for entry in known]
    return {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "root": str(root), "lang": language(), "strings": strings, "catalogs": catalogs,
            "version": VERSION, "run_token": run_token, "projects": projects, "active": active["name"],
            "lazy": not full,
            "reports": active["reports"],
            "docs": logics_bridge.documents(refs, root) if full else {},
            "runbooks": runbooks, "doctor": collect_doctor(root), "files": file_references(known),
            "ops_exists": active["ops_exists"],
            # Baked in rather than fetched, so a page opened from the filesystem shows what a
            # person wrote even though it has no server to ask. Voir adr_009.
            "notes": notes.read(root)}


def file_id(path: str) -> str:
    return hashlib.sha256(path.encode("utf-8")).hexdigest()[:16]


def file_references(projects: list[dict]) -> list[dict]:
    paths_seen = {}
    for project in projects:
        for report in project["reports"]:
            for value in ((report.get("input") or {}).get("path"), (report.get("output") or {}).get("path")):
                if value:
                    paths_seen[value] = {"id": file_id(value), "path": value}
            for render in report.get("renders", []):
                if render.get("path"):
                    paths_seen[render["path"]] = {"id": file_id(render["path"]), "path": render["path"]}
            for pair in report.get("comparisons", []):
                for key in ("before", "after"):
                    if pair.get(key):
                        paths_seen[pair[key]] = {"id": file_id(pair[key]), "path": pair[key]}
    return sorted(paths_seen.values(), key=lambda item: item["path"])


def resolve_file(root: Path, file_id_value: str) -> Path | None:
    target = root / OUT
    for item in file_references([{"reports": collect(project, target)} for project in paths.projects(root)]):
        if item["id"] == file_id_value:
            path = Path(item["path"])
            return path if path.exists() else None
    return None


ASSETS = ("viewer.css", "viewer.js", "icon.png", "index.html")


def stamped(index: str) -> str:
    """The page, with a cache-buster on everything a browser would otherwise keep.

    The script carried one and the stylesheet did not, so a rebuilt viewer arrived as new
    behaviour wearing the old layout: the project screen rendered its rows in a row, because
    the rules that stack them were in a stylesheet the browser had already cached. One stamp,
    both files -- they are rebuilt together and there is no case where one is fresh alone.
    """
    stamp = str(int(time.time()))
    return (index.replace('src="viewer.js"', f'src="viewer.js?v={stamp}"')
                 .replace('href="viewer.css"', f'href="viewer.css?v={stamp}"'))


def refresh_assets(root: Path) -> list[str]:
    """Copy the installed page over a project's stale copy, and say what moved.

    The served page is a copy under the project, so a rebuilt viewer reached nobody until the
    next `meshanvil view` -- the running server went on serving the bundle it was started
    with, and the operator had no reason to suspect a command was needed. The live route
    calls this, which is what lets a rebuilt page arrive on its own.
    """
    target = root / OUT
    if not target.is_dir():
        return []
    moved = []
    for name in ASSETS:
        source = paths.asset_root("viewer") / name
        copy = target / name
        try:
            # Only what a build already put there: refreshing is not building, and a page
            # half-populated by a background loop is a worse state than one not built yet.
            if not source.is_file() or not copy.is_file():
                continue
            if copy.stat().st_mtime_ns >= source.stat().st_mtime_ns:
                continue
            # index.html is rewritten rather than copied: it carries the cache-buster that
            # makes a browser fetch the new bundle instead of the one it already holds.
            if name == "index.html":
                copy.write_text(stamped(source.read_text(encoding="utf-8")), encoding="utf-8")
            else:
                shutil.copyfile(source, copy)
            moved.append(name)
        except OSError:
            continue
    return moved


def build(root: Path, run_token: str | None = None) -> tuple[Path, dict]:
    target = root / OUT
    target.mkdir(parents=True, exist_ok=True)
    for name in ("viewer.css", "viewer.js", "icon.png"):
        shutil.copyfile(paths.asset_root("viewer") / name, target / name)
    (target / "index.html").write_text(
        stamped((paths.asset_root("viewer") / "index.html").read_text(encoding="utf-8")),
        encoding="utf-8")
    data = payload(root, target, run_token)
    (target / "data.js").write_text(
        "window.MESHANVIL = " + json.dumps(data, indent=1) + ";\n", encoding="utf-8")
    return target / "index.html", data

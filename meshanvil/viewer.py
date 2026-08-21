"""Generate the viewer: the reports as one data file, next to a static page.

A page opened from file:// cannot fetch a neighbouring JSON -- browsers refuse it as a
cross-origin request -- but it can load a classic script. That is why the reports are written
as an assignment rather than served. `--serve` exists for auto-refresh; see adr_004.
"""
from __future__ import annotations
import functools, http.server, json, os, shutil, socketserver, subprocess, sys, time, webbrowser
from pathlib import Path

from . import manifests
from .engines import in_wsl
from .i18n import SOURCE, catalogue, language, t

OPS = "work/ops"
OUT = "work/viewer"


def collect(root: Path) -> list[dict]:
    """Every readable report, in identity order. An unreadable one is skipped, not fatal."""
    reports = []
    for path in sorted((root / OPS).glob("*.json")):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if report.get("id"):
            reports.append(with_render_urls(root, report))
    reports.sort(key=lambda r: (r["id"].rstrip("abcdefghijklmnopqrstuvwxyz"), r["id"]))
    return reports


def with_render_urls(root: Path, report: dict) -> dict:
    """The page lives in work/viewer/, so a render is reached relative to it."""
    for render in report.get("renders", []):
        try:
            render["url"] = os.path.relpath(render["path"], root / OUT)
        except ValueError:
            render["url"] = render["path"]
    return report


def collect_doctor(root: Path) -> dict | None:
    """The viewer only reads the last setup check; it never reruns one."""
    try:
        value = json.loads((root / "work" / "doctor.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def build(root: Path) -> Path:
    target = root / OUT
    target.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "viewer.css", "viewer.js"):
        shutil.copyfile(root / "viewer" / name, target / name)
    strings = {**catalogue(SOURCE), **catalogue(language())}   # English is the fallback
    payload = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "root": str(root), "lang": language(), "strings": strings,
               "reports": collect(root), "doctor": collect_doctor(root),
               "ops_exists": (root / OPS).is_dir()}
    (target / "data.js").write_text(
        "window.MESHANVIL = " + json.dumps(payload, indent=1) + ";\n", encoding="utf-8")
    return target / "index.html"


def open_in_browser(page: Path) -> None:
    """WSL is the exception: wslview is usually absent and xdg-open has no browser behind it."""
    if in_wsl():
        windows = subprocess.run(["wslpath", "-w", str(page)], capture_output=True,
                                 text=True, check=False).stdout.strip()
        subprocess.run(["explorer.exe", windows], check=False)
        return
    webbrowser.open(page.as_uri())


def serve(directory: Path) -> None:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        print(t("view.serving", port=port))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print()


def view(serve_it: bool = False, open_it: bool = True) -> int:
    root = manifests.root()
    page = build(root)
    count = len(json.loads(
        (page.parent / "data.js").read_text(encoding="utf-8").split("= ", 1)[1].rstrip(";\n")
    )["reports"])
    print(t("view.built", path=page.relative_to(root), count=count))
    if serve_it:
        if open_it:
            print(t("view.open_address"))
        serve(page.parent)
        return 0
    if open_it:
        open_in_browser(page)
    return 0

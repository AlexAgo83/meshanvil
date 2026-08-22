"""Generate the viewer: the reports as one data file, next to a static page.

A page opened from file:// cannot fetch a neighbouring JSON -- browsers refuse it as a
cross-origin request -- but it can load a classic script. That is why the reports are written
as an assignment rather than served. `--serve` exists for auto-refresh; see adr_004.
"""
from __future__ import annotations
import functools, http.server, json, os, secrets, shutil, subprocess, sys, threading, time, webbrowser
from pathlib import Path

from . import VERSION, logics_bridge, manifests, paths
from .engines import in_wsl
from .i18n import SOURCE, catalogue, language, t

OPS = "work/ops"
OUT = "work/viewer"

# adr_007: the closed command set a served page may run. A name from the page selects one of
# these argument lists; nothing the page sends ever becomes part of the command line itself.
RUNNABLE = {"list": ["list"], "doctor": ["doctor"], "prune": ["prune", "--dry-run"]}


def collect(root: Path, page: Path) -> list[dict]:
    """Every readable report of one project, in identity order.

    `page` is where the built page will sit, which is not always inside `root`: a render of
    another project is reached from the active project's page, so the relative path is
    computed against the page and never against the project it came from.
    """
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
    """A render is reached relative to the page that shows it, wherever it was written."""
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
    """The viewer only reads the last setup check; it never reruns one."""
    try:
        value = json.loads((root / "work" / "doctor.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def build(root: Path, run_token: str | None = None) -> Path:
    target = root / OUT
    target.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "viewer.css", "viewer.js", "icon.png"):
        shutil.copyfile(paths.code_root() / "viewer" / name, target / name)
    strings = {**catalogue(SOURCE), **catalogue(language())}   # English is the fallback
    # Every catalogue, so Help can switch language in the page without a rebuild -- the same
    # reason every project is read at build time instead of one at a time.
    catalogs = {code.stem: catalogue(code.stem) for code in sorted((paths.code_root() / "locales").glob("*.json"))}
    # Every project is read at build time. The page can then switch between them without a
    # request, a rebuild or a write, which is the only way it stays what adr_003 says it is.
    known = []
    for project in paths.projects(root):
        known.append({"name": paths.name(project), "path": str(project),
                      "reports": collect(project, target),
                      "ops_exists": (project / OPS).is_dir()})
    # projects() puts the active root first, reports or not. The page opens on the first one
    # that has something to show: a page that opens on an empty project because that is where
    # the command was typed sends a reader to the splash while the reports sit one click away.
    # The splash still states where a run would land, which is the question the root answers.
    active = next((entry for entry in known if entry["reports"]), known[0])
    runbooks = logics_bridge.runbooks(paths.code_root())
    # A report links only the docs it applied. A runbook nobody has applied yet is still
    # listed (that's the point -- a dormant method stays visible), so reading it from the
    # list needs its content fetched here too, not just the ones a report already points to.
    refs = {ref for entry in known for report in entry["reports"]
            for ref in report.get("links", {}).get("docs", [])}
    refs |= {doc["ref"] for doc in runbooks}
    payload = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "root": str(root), "lang": language(), "strings": strings, "catalogs": catalogs,
               "version": VERSION, "run_token": run_token, "projects": known, "active": active["name"],
               "reports": active["reports"], "docs": logics_bridge.documents(refs),
               "runbooks": runbooks, "doctor": collect_doctor(root),
               "ops_exists": active["ops_exists"]}
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


def run_command(root: Path, name: str) -> dict:
    """adr_007: the same entry point a person would type, on the fixed argument list `name`
    names -- never on anything else the request carries."""
    args = RUNNABLE[name]
    completed = subprocess.run(
        [sys.executable, str(paths.code_root() / "bin" / "meshanvil"), *args],
        cwd=str(root), capture_output=True, text=True, timeout=120)
    return {"stdout": completed.stdout, "stderr": completed.stderr, "exit_code": completed.returncode}


def make_server(directory: Path, root: Path, token: str) -> http.server.ThreadingHTTPServer:
    """Split from `serve()` so a test can start it, hit it, and shut it down without living
    inside `serve_forever()`. ThreadingHTTPServer, not the single-threaded TCPServer file
    serving used before: the single-flight lock below only refuses a genuinely concurrent
    request. A server that handled one connection at a time would just queue the second
    click behind the first, which is not what adr_007 decided."""
    lock = threading.Lock()

    class RunHandler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            if self.path != "/run":
                self.send_error(404, "not found")
                return
            if self.headers.get("X-Meshanvil-Token") != token:
                self.send_error(401, "bad or missing token")
                return
            length = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                self.send_error(400, "malformed request body")
                return
            if body.get("command") not in RUNNABLE:
                self.send_error(400, "unknown command")
                return
            if not lock.acquire(blocking=False):
                self.send_error(409, "a command is already running")
                return
            try:
                result = run_command(root, body["command"])
            finally:
                lock.release()
            payload = json.dumps(result).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

    handler = functools.partial(RunHandler, directory=str(directory))
    return http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)


def serve(directory: Path, root: Path, token: str, entry: str) -> None:
    with make_server(directory, root, token) as server:
        port = server.server_address[1]
        print(t("view.serving", port=port, entry=entry))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print()


def view(serve_it: bool = False, open_it: bool = True) -> int:
    root = paths.work_root()
    token = secrets.token_urlsafe(24) if serve_it else None
    page = build(root, run_token=token)
    count = len(json.loads(
        (page.parent / "data.js").read_text(encoding="utf-8").split("= ", 1)[1].rstrip(";\n")
    )["reports"])
    print(t("view.built", path=page.relative_to(root), count=count))
    if serve_it:
        # adr_004: "It serves work/ read-only" -- serving only work/viewer/ (the page's own
        # directory) left every render under work/renders/ unreachable, since http.server
        # never serves above the directory it is given. work/ is the directory that holds
        # both, so it is the one that has to be the server's root.
        served_root = root / "work"
        if open_it:
            print(t("view.open_address"))
        serve(served_root, root, token, str(page.relative_to(served_root)))
        return 0
    if open_it:
        open_in_browser(page)
    return 0

"""Public entry point for building or serving the viewer."""
from __future__ import annotations
import secrets, subprocess
from pathlib import Path

from . import paths, viewer_host, viewer_payload, viewer_server
from .i18n import t
from .viewer_routes.run import RUNNABLE, run_command

OPS = viewer_payload.OPS
OUT = viewer_payload.OUT

collect = viewer_payload.collect
with_render_urls = viewer_payload.with_render_urls
collect_doctor = viewer_payload.collect_doctor
make_server = viewer_server.make_server
serve = viewer_server.serve
open_in_browser = viewer_host.open_in_browser


def build(root: Path, run_token: str | None = None) -> Path:
    return viewer_payload.build(root, run_token)[0]


def view(serve_it: bool = True, open_it: bool = True, file_it: bool = False) -> int:
    root = paths.work_root()
    serve_it = serve_it and not file_it
    token = secrets.token_urlsafe(24) if serve_it else None
    page, data = viewer_payload.build(root, run_token=token)
    count = len(data["reports"])
    print(t("view.built", path=page.relative_to(root), count=count))
    if serve_it:
        served_root = root / "work"
        if open_it:
            print(t("view.open_address"))
        viewer_server.serve(served_root, root, token, str(page.relative_to(served_root)), open_it=open_it)
        return 0
    if open_it:
        viewer_host.open_in_browser(page)
    return 0

from __future__ import annotations

import json, subprocess, sys
import shutil
from urllib.parse import urlparse

from .. import doctor, manifests, paths

# adr_007: the closed command set a served page may run. A name from the page selects one of
# these argument lists; nothing the page sends ever becomes part of the command line itself.
RUNNABLE = {"list": ["list"], "doctor": ["doctor"], "prune": ["prune", "--dry-run"]}


def run_command(root, name: str) -> dict:
    if name == "list":
        found = manifests.discover()
        return {"stdout": "", "stderr": "", "exit_code": 0, "data": {"operations": found}}
    if name == "doctor":
        return {"stdout": "", "stderr": "", "exit_code": 0, "data": doctor.check(root)}
    args = RUNNABLE[name]
    command = shutil.which("meshanvil") or sys.executable
    prefix = [command] if command != sys.executable else [sys.executable, "-m", "meshanvil.cli"]
    completed = subprocess.run(
        [*prefix, *args],
        cwd=str(root), capture_output=True, text=True, timeout=120)
    return {"stdout": completed.stdout, "stderr": completed.stderr, "exit_code": completed.returncode}


def handle_post(handler, route: str, parsed: urlparse) -> bool:
    if route != "/run":
        return False
    if handler.headers.get("X-Meshanvil-Token") != handler.meshanvil_token:
        handler.send_error(401, "bad or missing token")
        return True
    length = int(handler.headers.get("Content-Length") or 0)
    try:
        body = json.loads(handler.rfile.read(length) or b"{}")
    except json.JSONDecodeError:
        handler.send_error(400, "malformed request body")
        return True
    if body.get("command") not in RUNNABLE:
        handler.send_error(400, "unknown command")
        return True
    if not handler.meshanvil_lock.acquire(blocking=False):
        handler.send_error(409, "a command is already running")
        return True
    try:
        result = run_command(handler.meshanvil_root, body["command"])
    finally:
        handler.meshanvil_lock.release()
    payload = json.dumps(result).encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)
    return True

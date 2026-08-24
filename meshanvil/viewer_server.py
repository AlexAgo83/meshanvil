"""HTTP server for the local viewer."""
from __future__ import annotations

import functools, hashlib, http.client, http.server, json, os, threading
from pathlib import Path
from urllib.parse import urlparse

from . import paths
from .i18n import t
from .viewer_host import open_in_browser
from .viewer_routes import ROUTES


def stable_port(root: Path) -> int:
    return 38000 + int(hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()[:4], 16) % 10000


def registry_path(root: Path) -> Path:
    return root / "work" / "viewer" / "server.json"


def lock_path(root: Path) -> Path:
    return root / "work" / "viewer" / "server.lock"


def ping(port: int, root: Path) -> bool:
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
        conn.request("GET", "/api/ping")
        response = conn.getresponse()
        data = json.loads(response.read() or b"{}")
        conn.close()
        return response.status == 200 and data.get("root") == str(root)
    except Exception:
        return False


def read_registry(root: Path) -> dict | None:
    try:
        data = json.loads(registry_path(root).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if ping(int(data.get("port", 0)), root) else None


def write_registry(root: Path, port: int, token: str) -> None:
    path = registry_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"root": str(root), "port": port, "token": token}, indent=1), encoding="utf-8")


def claim_lock(root: Path):
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        return os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
    except FileExistsError:
        if not read_registry(root):
            path.unlink(missing_ok=True)
            return os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        return None


def release_lock(root: Path, fd) -> None:
    if fd is not None:
        os.close(fd)
        lock_path(root).unlink(missing_ok=True)


def _loopback_host(value: str) -> bool:
    return value in {"127.0.0.1", "localhost", "::1"}


def make_server(directory: Path, root: Path, token: str, port: int = 0) -> http.server.ThreadingHTTPServer:
    lock = threading.Lock()

    class ViewerHandler(http.server.SimpleHTTPRequestHandler):
        meshanvil_root = root
        meshanvil_page = root / "work" / "viewer"
        meshanvil_token = token
        meshanvil_lock = lock

        def same_origin(self) -> bool:
            actual = self.server.server_address[1]
            host = self.headers.get("Host", "")
            parsed_host = urlparse(f"//{host}")
            try:
                host_port = parsed_host.port or 80
            except ValueError:
                return False
            if not (_loopback_host(parsed_host.hostname or "") and host_port == actual):
                return False
            origin = self.headers.get("Origin")
            if not origin:
                return True
            parsed_origin = urlparse(origin)
            return (parsed_origin.scheme == "http" and _loopback_host(parsed_origin.hostname or "")
                    and (parsed_origin.port or 80) == actual)

        def guard_origin(self) -> bool:
            if self.same_origin():
                return True
            self.send_error(403, "served viewer origin refused")
            return False

        def list_directory(self, path):
            self.send_error(404, "directory listing refused")
            return None

        def do_HEAD(self):
            # Inherited from SimpleHTTPRequestHandler, so it reaches the static tree on its own:
            # unguarded it answered the size and existence of every file under work/.
            if not self.guard_origin():
                return
            super().do_HEAD()

        def do_GET(self):
            if not self.guard_origin():
                return
            parsed = urlparse(self.path)
            # The server is rooted above work/ so renders resolve, which leaves "/" pointing at
            # a directory it refuses to list -- a 404 on the address anyone types first. The
            # page lives one level down; say so rather than making it be typed.
            if parsed.path in ("", "/"):
                self.send_response(302)
                self.send_header("Location", "/viewer/index.html")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            if parsed.path == "/api/ping":
                body = json.dumps({"root": str(root)}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            for route in ROUTES:
                if getattr(route, "handle_get", lambda *_: False)(self, parsed.path, parsed):
                    return
            super().do_GET()

        def do_POST(self):
            if not self.guard_origin():
                return
            parsed = urlparse(self.path)
            for route in ROUTES:
                if getattr(route, "handle_post", lambda *_: False)(self, parsed.path, parsed):
                    return
            self.send_error(404, "not found")

    handler = functools.partial(ViewerHandler, directory=str(directory))
    return http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)


def serve(directory: Path, root: Path, token: str, entry: str, port: int | None = None, open_it: bool = False) -> None:
    port = stable_port(root) if port is None else port
    fd = claim_lock(root)
    if fd is None:
        found = read_registry(root)
        if found:
            print(t("view.reusing", port=found["port"]))
            if open_it:
                open_in_browser(f"http://127.0.0.1:{found['port']}/viewer/index.html")
            return
    try:
        with make_server(directory, root, token, port) as server:
            actual = server.server_address[1]
            write_registry(root, actual, token)
            print(t("view.serving", port=actual, entry=entry))
            if open_it:
                open_in_browser(f"http://127.0.0.1:{actual}/{entry}")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print()
    except OSError as error:
        if error.errno in (48, 98):
            raise SystemExit(t("view.port_busy", port=port))
        raise
    finally:
        registry_path(root).unlink(missing_ok=True)
        release_lock(root, fd)

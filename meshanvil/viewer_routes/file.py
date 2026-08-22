from __future__ import annotations

import json
from urllib.parse import urlparse

from .. import viewer_host, viewer_payload


def handle_post(handler, route: str, parsed: urlparse) -> bool:
    if route != "/file":
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
    path = viewer_payload.resolve_file(handler.meshanvil_root, str(body.get("id", "")))
    action = body.get("action")
    if not path or action not in {"open", "reveal"}:
        handler.send_error(400, "unknown file action")
        return True
    if action == "open":
        viewer_host.open_file(path)
    else:
        viewer_host.reveal_file(path)
    body = b'{"ok":true}'
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)
    return True

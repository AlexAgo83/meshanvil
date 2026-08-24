"""The one route by which the page writes. Voir adr_009.

Guarded exactly like the two that already exist -- token, origin, host -- and narrower than
both: it takes no path from the request at all. The file it lands in is derived from the root
the server was launched with, and the only two things writable are a note on a report and a
name on a chain.
"""
from __future__ import annotations

import json, threading
from urllib.parse import urlparse

from .. import notes

# Writes are serialised the way the run route serialises its subprocess: the file is rewritten
# whole, so two concurrent writers would otherwise race over the same rename.
LOCK = threading.Lock()


def handle_post(handler, route: str, parsed: urlparse) -> bool:
    if route != "/note":
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
    kind, key = str(body.get("kind", "")), str(body.get("key", ""))
    text = body.get("text")
    if kind not in ("reports", "chains") or not key or not isinstance(text, str):
        handler.send_error(400, "an annotation is a text on a report or a chain")
        return True
    with LOCK:
        try:
            data = notes.put(handler.meshanvil_root, kind, key, text)
        except OSError:
            handler.send_error(500, "the annotation file could not be written")
            return True
    payload = json.dumps({"ok": True, "notes": data}).encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)
    return True

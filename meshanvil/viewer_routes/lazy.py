"""What the first paint left out, fetched when it is first needed.

Guarded like every other route here -- the origin and host checks run before any of this --
and read-only: neither takes a path, both name a thing the payload already told the page about.
"""
from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

from .. import logics_bridge, paths, viewer_payload


def _send(handler, data: dict) -> None:
    body = json.dumps(data).encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def handle_get(handler, route: str, parsed: urlparse) -> bool:
    if route == "/api/project":
        name = (parse_qs(parsed.query).get("name") or [""])[0]
        # The name is matched against the neighbourhood the server itself computed: a name that
        # is not one of those resolves to nothing, so no request can name a directory.
        found = next((project for project in paths.projects(handler.meshanvil_root)
                      if paths.name(project) == name), None)
        if not found:
            handler.send_error(404, "no such project")
            return True
        _send(handler, {"name": name, "path": str(found),
                        "reports": viewer_payload.collect(found, handler.meshanvil_page),
                        "ops_exists": (found / viewer_payload.OPS).is_dir()})
        return True
    if route == "/api/doc":
        ref = (parse_qs(parsed.query).get("ref") or [""])[0]
        documents = logics_bridge.documents({ref}, handler.meshanvil_root) if ref else {}
        if ref not in documents:
            handler.send_error(404, "no such document")
            return True
        _send(handler, {"ref": ref, "doc": documents[ref]})
        return True
    return False

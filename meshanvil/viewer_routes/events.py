from __future__ import annotations

import json, time
from pathlib import Path
from urllib.parse import urlparse

from .. import logics_bridge, paths, viewer_payload


def _stamp(paths: list[Path]) -> tuple:
    out = []
    for path in paths:
        try:
            stat = path.stat()
        except OSError:
            continue
        out.append((str(path), stat.st_mtime_ns, stat.st_size))
    return tuple(out)


def signatures(root: Path) -> dict[str, tuple]:
    reports = sorted((root / viewer_payload.OPS).glob("*.json"))
    runbooks = [Path(doc["path"]) for doc in logics_bridge.runbooks(paths.code_root()) if doc.get("path")]
    return {
        "reports": _stamp(reports),
        "doctor": _stamp([root / "work" / "doctor.json"]),
        "runbooks": _stamp(runbooks),
    }


def handle_get(handler, route: str, parsed: urlparse) -> bool:
    if route != "/api/events":
        return False
    handler.send_response(200)
    handler.send_header("Content-Type", "text/event-stream")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Connection", "keep-alive")
    handler.end_headers()
    last = signatures(handler.meshanvil_root)
    handler.wfile.write(b": connected\n\n")
    handler.wfile.flush()
    try:
        while True:
            started = time.perf_counter()
            current = signatures(handler.meshanvil_root)
            changed = [name for name, value in current.items() if value != last.get(name)]
            if changed:
                last = current
                payload = json.dumps({"components": changed})
                handler.wfile.write(f"event: changed\ndata: {payload}\n\n".encode("utf-8"))
                handler.wfile.flush()
            # ponytail: mtime polling; switch to platform watchers only if idle polling shows up in profiles.
            time.sleep(max(1.0, (time.perf_counter() - started) * 20))
    except (BrokenPipeError, ConnectionError, OSError):
        return True
    return True

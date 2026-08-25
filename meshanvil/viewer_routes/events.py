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


# How often the server looks for a change, in seconds. One number, so the page's liveness is
# a property of this route rather than of the project's size.
INTERVAL = 1.0


def signatures(root: Path) -> dict[str, tuple]:
    reports = sorted((root / viewer_payload.OPS).glob("*.json"))
    runbooks = [root / doc["path"] for doc in logics_bridge.runbooks(root) if doc.get("path")]
    # The page's own code, not only the data it draws. A page holds the bundle it loaded at
    # open, so a viewer change was invisible until someone thought to reload -- while report
    # changes had been arriving live all along, which is exactly what makes it not occur to
    # anyone. This is the one component the page answers by reloading itself.
    page = root / "work" / "viewer"
    assets = [page / name for name in ("viewer.js", "viewer.css", "index.html")]
    return {
        "reports": _stamp(reports),
        "doctor": _stamp([root / "work" / "doctor.json"]),
        "runbooks": _stamp(runbooks),
        "viewer": _stamp(assets),
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
            else:
                handler.wfile.write(b": poll\n\n")
            handler.wfile.flush()
            # ponytail: mtime polling; switch to platform watchers only if idle polling shows up
            # in profiles.
            #
            # A declared interval, not a multiple of the scan's own cost. Sleeping for twenty
            # times the scan made the cadence a function of how much there was to watch: with
            # eight sibling projects the scan is dear and the viewer answered slowest exactly
            # when it had most to say. The scan's duration is subtracted so the period holds
            # whatever it costs, and a scan dearer than the period simply runs back to back.
            time.sleep(max(0.0, INTERVAL - (time.perf_counter() - started)))
    except (BrokenPipeError, ConnectionError, OSError):
        return True
    return True

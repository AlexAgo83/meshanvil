from __future__ import annotations

import json
from urllib.parse import urlparse

from .. import viewer_payload


def handle_get(handler, route: str, parsed: urlparse) -> bool:
    if route != "/api/data":
        return False
    # The served page can ask for the rest; the snapshot on disk cannot, and stays full.
    body = json.dumps(viewer_payload.payload(handler.meshanvil_root, handler.meshanvil_page,
                                             handler.meshanvil_token, full=False)).encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)
    return True

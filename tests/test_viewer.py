import http.client
import json
import threading
from pathlib import Path

from scripts import selfcheck
from meshanvil import viewer_payload, viewer_server
from meshanvil.viewer_routes import run


def test_viewer_start(tmp_path: Path):
    selfcheck.check_viewer_start(tmp_path)


def test_run_endpoint(tmp_path: Path):
    selfcheck.check_run_endpoint(tmp_path)


def test_viewer_origin_and_listing(tmp_path: Path):
    selfcheck.check_viewer_origin_and_listing(tmp_path)


def test_first_paint_carries_what_it_draws(tmp_path: Path):
    selfcheck.check_first_paint_carries_what_it_draws(tmp_path)


def test_annotations_stay_out_of_the_reports(tmp_path: Path):
    selfcheck.check_annotations_stay_out_of_the_reports(tmp_path)


def test_events_cadence_is_declared(tmp_path: Path):
    selfcheck.check_events_cadence_is_declared(tmp_path)


def test_events_releases_gone_peer(tmp_path: Path):
    selfcheck.check_events_releases_gone_peer(tmp_path)


def test_viewer_comparison_layout():
    selfcheck.check_viewer_comparison_layout()


def test_viewer_stable_port(tmp_path: Path):
    first = tmp_path / "one"
    second = tmp_path / "two"
    first.mkdir()
    second.mkdir()
    assert viewer_server.stable_port(first) == viewer_server.stable_port(first)
    assert viewer_server.stable_port(first) != viewer_server.stable_port(second)


def test_stale_viewer_lock_is_reclaimed(tmp_path: Path):
    root = tmp_path / "project"
    (root / "work" / "viewer").mkdir(parents=True)
    viewer_server.lock_path(root).write_text("stale", encoding="utf-8")
    fd = viewer_server.claim_lock(root)
    try:
        assert fd is not None
    finally:
        viewer_server.release_lock(root, fd)


def test_file_endpoint_uses_known_file_ids(tmp_path: Path, monkeypatch):
    root = tmp_path / "project"
    asset = root / "work" / "renders" / "001.png"
    asset.parent.mkdir(parents=True)
    asset.write_bytes(b"png")
    (root / "work" / "ops").mkdir(parents=True)
    (root / "work" / "ops" / "001_test.json").write_text(
        json.dumps({"id": "001", "renders": [{"path": str(asset)}]}), encoding="utf-8")
    calls = []
    monkeypatch.setattr("meshanvil.viewer_host.open_file", lambda path: calls.append(("open", path)))
    monkeypatch.setattr("meshanvil.viewer_host.reveal_file", lambda path: calls.append(("reveal", path)))
    server = viewer_server.make_server(root, root, "token")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        def post(body, token="token"):
            conn = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
            conn.request("POST", "/file", body=json.dumps(body), headers={"X-Meshanvil-Token": token})
            response = conn.getresponse()
            response.read()
            conn.close()
            return response.status

        assert post({"id": viewer_payload.file_id(str(asset)), "action": "open"}) == 200
        assert calls == [("open", asset)]
        assert post({"id": str(asset), "action": "reveal"}) == 400
        assert post({"id": viewer_payload.file_id(str(asset)), "action": "reveal"}, token="bad") == 401
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_run_list_and_doctor_are_structured(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(run.manifests, "discover", lambda: {"op": {"operation": "op"}})
    monkeypatch.setattr(run.doctor, "check", lambda root: {"ok": True, "requirements": []})
    assert run.run_command(tmp_path, "list") == {
        "stdout": "", "stderr": "", "exit_code": 0, "data": {"operations": {"op": {"operation": "op"}}}}
    assert run.run_command(tmp_path, "doctor") == {
        "stdout": "", "stderr": "", "exit_code": 0, "data": {"ok": True, "requirements": []}}

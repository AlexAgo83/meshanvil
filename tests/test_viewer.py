from pathlib import Path

from scripts import selfcheck
from meshanvil import viewer_server


def test_viewer_start(tmp_path: Path):
    selfcheck.check_viewer_start(tmp_path)


def test_run_endpoint(tmp_path: Path):
    selfcheck.check_run_endpoint(tmp_path)


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

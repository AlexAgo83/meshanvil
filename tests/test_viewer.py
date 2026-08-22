from pathlib import Path

from scripts import selfcheck


def test_viewer_start(tmp_path: Path):
    selfcheck.check_viewer_start(tmp_path)


def test_run_endpoint(tmp_path: Path):
    selfcheck.check_run_endpoint(tmp_path)


def test_viewer_comparison_layout():
    selfcheck.check_viewer_comparison_layout()

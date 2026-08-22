from pathlib import Path

from scripts import selfcheck


def test_engine_floor():
    selfcheck.check_engine_floor()


def test_wsl_boundary(tmp_path: Path):
    selfcheck.check_wsl_boundary(tmp_path)

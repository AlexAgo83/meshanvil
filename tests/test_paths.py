from pathlib import Path

from scripts import selfcheck


def test_projects(tmp_path: Path):
    selfcheck.check_projects(tmp_path)

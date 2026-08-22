from pathlib import Path

from scripts import selfcheck


def test_prune(tmp_path: Path):
    selfcheck.check_prune(tmp_path)

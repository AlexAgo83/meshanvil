from pathlib import Path

from scripts import selfcheck


def test_identity(tmp_path: Path):
    selfcheck.check_identity(tmp_path)


def test_parent(tmp_path: Path):
    (tmp_path / "work" / "ops").mkdir(parents=True)
    selfcheck.check_parent(tmp_path)


def test_refusals():
    selfcheck.check_refusals()


def test_target_lock(tmp_path: Path):
    selfcheck.check_target_lock(tmp_path)


def test_runner_interrupt_stops_engine(tmp_path: Path):
    selfcheck.check_runner_interrupt_stops_engine(tmp_path)

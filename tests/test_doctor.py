from pathlib import Path

from scripts import selfcheck


def test_doctor(tmp_path: Path):
    selfcheck.check_doctor(tmp_path)


def test_doctor_exit_code():
    selfcheck.check_doctor_exit_code()

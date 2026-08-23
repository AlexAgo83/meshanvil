from scripts import selfcheck


def test_cli_welcome():
    selfcheck.check_cli_welcome()


def test_cli_json(tmp_path):
    selfcheck.check_cli_json(tmp_path)


def test_cli_reports(tmp_path):
    selfcheck.check_cli_reports(tmp_path)


def test_cli_status(tmp_path):
    selfcheck.check_cli_status(tmp_path)


def test_cli_schema():
    selfcheck.check_cli_schema()


def test_demo_command(tmp_path):
    selfcheck.check_demo_command(tmp_path)

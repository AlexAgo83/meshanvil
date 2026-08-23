from scripts import selfcheck


def test_cli_welcome():
    selfcheck.check_cli_welcome()


def test_cli_json(tmp_path):
    selfcheck.check_cli_json(tmp_path)

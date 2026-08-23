"""Every operation manifest must carry its summary in both catalogues, or `list` prints a key."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_every_op_has_a_summary_in_every_locale():
    manifests = sorted(ROOT.joinpath("tools").glob("*.op.json"))
    assert manifests, "no operation manifests found"
    for locale in ("en", "fr"):
        catalogue = json.loads(ROOT.joinpath("locales", f"{locale}.json").read_text(encoding="utf-8"))
        for path in manifests:
            key = json.loads(path.read_text(encoding="utf-8"))["summary_key"]
            node = catalogue
            for part in key.split("."):
                assert part in node, f"{locale}.json has no {key} for {path.name}"
                node = node[part]
            assert node.strip(), f"{locale}.json has an empty {key}"

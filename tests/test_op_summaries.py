"""Every operation manifest must carry its summary in both catalogues, or `list` prints a key."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_every_op_has_a_summary_in_every_locale():
    # local_* is the convention for an operation that lives in one checkout and is not part
    # of the tool: it ships no manifest, no strings and no fixture, and this rule is about
    # what the tool ships. `list` falls back to the key for those, which is what they get.
    manifests = [p for p in sorted(ROOT.joinpath("tools").glob("*.op.json"))
                 if not p.name.startswith("local_")]
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

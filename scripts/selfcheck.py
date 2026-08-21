#!/usr/bin/env python3
"""The smallest thing that fails if the host logic breaks. No Blender, no framework.

Covers what is easy to get quietly wrong: identity allocation under collision, parameter
resolution, the bounding-box delta, and the refusals that must leave work/ops untouched.
"""
import json, shutil, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from meshanvil import manifests, runner            # noqa: E402
from meshanvil_engine.report import bbox_delta     # noqa: E402


def check_parameters():
    manifest = {"operation": "x", "params": [
        {"name": "ratio", "type": "float", "default": 2.5},
        {"name": "fix", "type": "bool", "default": False}]}
    assert manifests.resolve(manifest, {}) == {"ratio": 2.5, "fix": False}
    assert manifests.resolve(manifest, {"ratio": "3"}) == {"ratio": 3.0, "fix": False}
    assert manifests.resolve(manifest, {"fix": "true"})["fix"] is True
    try:
        manifests.resolve(manifest, {"voxel": "3"})
        raise AssertionError("an unknown parameter must be refused")
    except KeyError:
        pass


def check_identity(tmp: Path):
    (tmp / "work" / "ops").mkdir(parents=True)
    first, path_a = runner.allocate(tmp, "op", None)
    assert first == "001", first
    second, _ = runner.allocate(tmp, "op", None)
    assert second == "002", second          # a claimed identity is never handed out twice
    path_a.write_text(json.dumps({"id": "001", "links": {"parent": None}}), encoding="utf-8")
    child, path_c = runner.allocate(tmp, "op", "001")
    assert child == "003", child            # first child keeps a bare ordinal
    path_c.write_text(json.dumps({"id": child, "links": {"parent": "001"}}), encoding="utf-8")
    sibling, _ = runner.allocate(tmp, "op", "001")
    assert sibling == "003a", sibling       # a second child of the same parent takes a letter


def check_parent(tmp: Path):
    report = tmp / "work" / "ops" / "010_op.json"
    report.write_text(json.dumps({"id": "010", "output": {"sha256": "abc"}}), encoding="utf-8")
    assert runner.resolve_parent(tmp, "abc") == "010"
    assert runner.resolve_parent(tmp, "nope") is None


def check_bbox_delta():
    before = {"bbox_mm": {"min": [-268.0, -247.2, 52.5], "max": [4.4, 127.5, 194.8]}}
    after = {"bbox_mm": {"min": [-268.0, 22.5, 52.5], "max": [-205.1, 127.5, 157.5]}}
    delta = bbox_delta(before, after)
    assert delta["axes_moved"] == ["X", "Y", "Z"], delta
    same = bbox_delta(before, before)
    assert same["axes_moved"] == [], same   # an unchanged box must report no movement
    assert bbox_delta({}, after) is None


def check_refusals():
    for arguments in (["run", "nope", "README.md"],
                      ["run", "scan_defects", "does-not-exist.blend"]):
        from meshanvil import cli
        assert cli.main(arguments) == runner.EXIT_REFUSED, arguments


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="meshanvil-selfcheck-"))
    try:
        check_parameters()
        check_identity(tmp)
        check_parent(tmp)
        check_bbox_delta()
        check_refusals()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("selfcheck: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

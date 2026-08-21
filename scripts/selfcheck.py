#!/usr/bin/env python3
"""The smallest thing that fails if the host logic breaks. No Blender, no framework.

Covers what is easy to get quietly wrong: identity allocation under collision, parameter
resolution, the bounding-box delta, and the refusals that must leave work/ops untouched.
"""
import json, os, shutil, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from meshanvil import doctor, engines, i18n, manifests, runner  # noqa: E402
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
    try:
        manifests.resolve(manifest, {"ratio": "nope"})
        raise AssertionError("an invalid parameter must be refused")
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
    sibling, path_s = runner.allocate(tmp, "op", "001")
    assert sibling == "003a", sibling       # a second child of the same parent takes a letter
    path_s.write_text(json.dumps({"id": sibling, "links": {"parent": "001"}}), encoding="utf-8")
    other, _ = runner.allocate(tmp, "other", "001")
    assert other == "003b", other           # an identity is taken whatever operation wrote it


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


def check_i18n():
    previous = os.environ.get("MESHANVIL_LANG")
    original_locale, original_catalogue = i18n.locale.getlocale, i18n.catalogue
    try:
        os.environ["MESHANVIL_LANG"] = "fr_FR"
        assert i18n.language() == "fr"
        os.environ.pop("MESHANVIL_LANG")
        i18n.locale.getlocale = lambda: ("fr_FR", "UTF-8")
        assert i18n.language() == "fr"
        os.environ["MESHANVIL_LANG"] = "fr"
        i18n.catalogue = lambda lang: {"fallback": "English"} if lang == "en" else {}
        key = "fallback"
        assert i18n.t(key) == "English"
    finally:
        i18n.locale.getlocale, i18n.catalogue = original_locale, original_catalogue
        if previous is None:
            os.environ.pop("MESHANVIL_LANG", None)
        else:
            os.environ["MESHANVIL_LANG"] = previous


def check_doctor(tmp: Path):
    binary = tmp / "blender"
    binary.write_text("", encoding="utf-8")
    original_find, original_version = engines.find, engines.version
    calls = []
    try:
        engines.find = lambda name: binary if name == "blender" else (_ for _ in ()).throw(engines.EngineMissing())
        engines.version = lambda path: (calls.append(path) or ("5.2.0", ""))
        result = doctor.check(tmp)
        assert result["ok"] is True
        assert [item["state"] for item in result["requirements"]] == ["found", "missing", "found"]
        assert [item["class"] for item in result["requirements"]] == ["required", "optional", "required"]
        assert (tmp / "work" / "doctor.json").is_file()
        assert doctor.check(tmp)["next"] is None and len(calls) == 1
    finally:
        engines.find, engines.version = original_find, original_version


def check_engine_floor():
    try:
        engines.check_floor("blender", "4.1.0")
        raise AssertionError("an old Blender must be refused")
    except engines.EngineMissing as error:
        assert "bpy.ops.wm.stl_export" in str(error) and "MESHANVIL_BLENDER" in str(error)
    assert "MESHANVIL_BLENDER" in engines.fix_command("blender")


def check_doctor_exit_code():
    from meshanvil import cli
    original = doctor.check
    try:
        doctor.check = lambda root: {"ok": False, "requirements": []}
        assert cli.main(["doctor"]) == runner.EXIT_REFUSED
    finally:
        doctor.check = original


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="meshanvil-selfcheck-"))
    try:
        check_parameters()
        check_identity(tmp)
        check_parent(tmp)
        check_bbox_delta()
        check_refusals()
        check_i18n()
        check_doctor(tmp)
        check_engine_floor()
        check_doctor_exit_code()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("selfcheck: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

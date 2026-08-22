#!/usr/bin/env python3
"""Regenerate the demo scene and assert that the tools find the defects it was built with.

This is the ground truth the sweep never had: the scene is generated with a known smear and
known duplicates, so a regression shows up as a finding that stopped appearing rather than as
a number nobody compared. Needs Blender, so it is not part of `make check` -- run `make fixture`.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPS = ROOT / "work" / "ops"
BLENDER = os.environ.get("MESHANVIL_BLENDER",
                         "/Applications/Blender.app/Contents/MacOS/Blender")


def run(*arguments: str) -> int:
    return subprocess.run([sys.executable, str(ROOT / "bin" / "meshanvil"), *arguments],
                          capture_output=True, text=True).returncode


def report(identity: str) -> dict:
    matches = list(OPS.glob(f"{identity}_*.json"))
    assert len(matches) == 1, f"expected one report {identity}, found {len(matches)}"
    return json.loads(matches[0].read_text(encoding="utf-8"))


def finding(data: dict, code: str) -> dict:
    for item in data.get("findings", []):
        if item["code"] == code:
            return item
    raise AssertionError(f"{data['id']} has no finding {code}; it found "
                         f"{[f['code'] for f in data.get('findings', [])]}")


def main() -> int:
    if not Path(BLENDER).exists():
        print(f"blender not found at {BLENDER}; set MESHANVIL_BLENDER")
        return 2
    # The fixture chain is a correctness test, not the dataset the viewer ships. It used to
    # wipe work/ops and leave its own four reports behind, so whatever ran last decided what
    # the viewer showed. Put the demo chain back on the way out.
    kept = OPS.with_name("ops.kept")
    shutil.rmtree(kept, ignore_errors=True)
    if OPS.is_dir():
        OPS.rename(kept)
    try:
        return check()
    finally:
        shutil.rmtree(OPS, ignore_errors=True)
        if kept.is_dir():
            kept.rename(OPS)


def check() -> int:
    subprocess.run([BLENDER, "-b", "-P", str(ROOT / "tools" / "make_demo_scene.py")],
                   capture_output=True, text=True, check=True)
    source = ROOT / "work" / "out" / "demo_source.blend"
    target = ROOT / "work" / "out" / "fixture_check.blend"
    shutil.copyfile(source, target)

    assert run("run", "scan_defects", str(target)) == 0
    scan = report("001")
    smear = finding(scan, "smeared_island")
    assert smear["subject"] == "trim_R", smear
    assert smear["ratio"] >= 2.5, smear          # the sweep's own threshold, found unaided
    duplicates = finding(scan, "coincident_duplicates")
    assert duplicates["objects"] == 4, duplicates
    assert 0.35 < duplicates["share_of_vertices"] < 0.40, duplicates
    assert scan["measured"]["objects"] == 12, scan["measured"]

    assert run("run", "scan_defects", str(target), "--set", "fix=true") == 0
    dedupe = report("002")
    assert dedupe["kind"] == "transform", dedupe["kind"]
    assert dedupe["output"]["sha256"], "the host must complete the output fingerprint"

    # A coarse voxel destroys the detail while every topology check stays green: what says so
    # is the bounding box, and the operation turns that into an exit code.
    assert run("run", "voxel_remesh", str(target), "--set", "voxel_mm=30") == 1
    coarse = report("003")
    drift = max(abs(v) for v in coarse["bbox_delta_mm"]["min"] + coarse["bbox_delta_mm"]["max"])
    assert drift > 50, f"a 30 mm voxel should move the box far more than this: {drift} mm"
    assert coarse["after"]["vertices"] < coarse["before"]["vertices"] / 10, coarse["after"]
    assert coarse["links"]["parent"] == "002", coarse["links"]
    assert coarse["links"]["parent_source"] == "fingerprint", coarse["links"]
    assert len(coarse["comparisons"]) == 4, coarse.get("comparisons")
    assert all(pair["camera"].endswith("-subject") for pair in coarse["comparisons"])
    assert all(Path(pair["before"]).is_file() and Path(pair["after"]).is_file()
               for pair in coarse["comparisons"])
    # The before copy exists to shoot the comparison, not to travel in the artefact: left in,
    # it is the heaviest object in the file and the next operation works on it by mistake.
    assert coarse["params"]["artefact_objects"] == 1, coarse["params"]

    assert run("run", "ray_visibility", str(target), "--set", "grid=40") == 0
    rays = report("003a")                         # a sibling of the same parent takes a letter
    visibility = finding(rays, "visibility")
    assert visibility["seen"] == 8, visibility    # the demo has no internal part to hide
    assert visibility["never_seen"] == 0, visibility

    # --- the guards, on a subject whose thinnest feature is known exactly ---
    subprocess.run([BLENDER, "-b", "-P", str(ROOT / "tools" / "make_guard_fixture.py")],
                   capture_output=True, text=True, check=True)
    slab = ROOT / "work" / "out" / "guard_fixture.blend"

    # A 100 x 100 x 2 mm box: one object, so the smallest object extent is the whole subject.
    # The two measures answering the same number is the bug this asserts against.
    assert run("run", "voxel_remesh", str(slab), "--set", "voxel_mm=0.5",
               "--set", "render=false", "--set", "max_bbox_drift_mm=5") == 0
    fine = report("004")
    assert fine["params"]["smallest_input_extent_mm"] >= 99.0, fine["params"]
    thin = fine["params"]["thin_feature_mm"]
    assert thin is not None and 1.8 <= thin <= 2.2, f"thinnest feature read as {thin} mm, not 2"
    assert fine["params"]["thin_feature_is_estimate"] is True, fine["params"]
    assert "thin_feature_below_voxel_floor" not in fine["warnings"], fine["warnings"]

    # Four voxels across the slab keeps it; two thirds of one does not, and only the guard
    # says so -- the topology checks pass either way.
    assert run("run", "voxel_remesh", str(slab), "--set", "voxel_mm=3",
               "--set", "render=false", "--set", "max_bbox_drift_mm=9") == 0
    coarse = report("005")
    assert "thin_feature_below_voxel_floor" in coarse["warnings"], coarse["warnings"]
    erased = finding(coarse, "thin_feature")
    assert erased["voxels_across"] < 2.0, erased

    # A volume with a pinhole is not an open panel. A zero test walls it and hollows it; the
    # slab cannot show this, because a perfectly closed body takes the branch that was always
    # right. Four boundary edges out of 992 is the shape of the defect seen on a sculpt.
    pinhole = ROOT / "work" / "out" / "guard_pinhole.blend"
    assert run("run", "solidify", str(pinhole), "--set", "thickness_mm=1",
               "--set", "render=false") == 0
    walling = report("006")
    assert walling["before"]["vertices"] == walling["after"]["vertices"], \
        f"a body with a pinhole was thickened: {walling['before']['vertices']} -> {walling['after']['vertices']}"
    decided = finding(walling, "walling_decisions")
    assert decided["walled"] == 0, decided
    assert decided["sealed"] == 1, decided
    # measure_scene leaves what an operation did not measure null, so the closure the
    # operation did measure is what says the pinhole is gone.
    closure = finding(walling, "closure")
    assert closure["closed_after"] == closure["total"] == 1, closure

    # A format the operation cannot read is refused before an engine is launched, so no
    # identity is claimed and nothing is written.
    before_refusal = sorted(OPS.glob("*.json"))
    assert run("run", "import_mesh", str(ROOT / "README.md")) == 2
    assert sorted(OPS.glob("*.json")) == before_refusal, "a refusal claimed an identity"

    identities = [json.loads(p.read_text(encoding="utf-8"))["id"] for p in OPS.glob("*.json")]
    assert len(identities) == len(set(identities)), f"identities collided: {identities}"

    slab.unlink(missing_ok=True)
    pinhole.unlink(missing_ok=True)
    for pattern in ("guard_fixture_*.blend", "guard_pinhole_*.blend"):
        for leftover in (ROOT / "work" / "out").glob(pattern):
            leftover.unlink(missing_ok=True)
    target.unlink(missing_ok=True)
    print(f"fixture: ok ({len(identities)} reports, defects found unaided)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

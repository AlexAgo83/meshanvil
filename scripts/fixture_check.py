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
    shutil.rmtree(OPS, ignore_errors=True)
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
    assert run("run", "voxel_remesh", str(target), "--set", "voxel_mm=30",
               "--set", "render=false") == 1
    coarse = report("003")
    drift = max(abs(v) for v in coarse["bbox_delta_mm"]["min"] + coarse["bbox_delta_mm"]["max"])
    assert drift > 50, f"a 30 mm voxel should move the box far more than this: {drift} mm"
    assert coarse["after"]["vertices"] < coarse["before"]["vertices"] / 10, coarse["after"]
    assert coarse["links"]["parent"] == "002", coarse["links"]
    assert coarse["links"]["parent_source"] == "fingerprint", coarse["links"]

    assert run("run", "ray_visibility", str(target), "--set", "grid=40") == 0
    rays = report("003a")                         # a sibling of the same parent takes a letter
    visibility = finding(rays, "visibility")
    assert visibility["seen"] == 8, visibility    # the demo has no internal part to hide
    assert visibility["never_seen"] == 0, visibility

    identities = [json.loads(p.read_text(encoding="utf-8"))["id"] for p in OPS.glob("*.json")]
    assert len(identities) == len(set(identities)), f"identities collided: {identities}"

    target.unlink(missing_ok=True)
    print(f"fixture: ok ({len(identities)} reports, defects found unaided)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

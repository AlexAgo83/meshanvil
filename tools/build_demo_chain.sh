#!/usr/bin/env bash
# Rebuild the demonstration dataset: the shipped asset, then the real operations run through
# the real CLI. Nothing here fabricates a report -- every number in work/ops/ comes out of
# Blender, which is the whole point of the viewer.
#
# fixtures/demo_car.blend is a render asset, not a CAD model, and that is the scenario: it
# carries every failure a printing pipeline runs into, none of them planted. Each step below
# is where one of them surfaces, and the branch is where skipping a step destroys the model
# with every topology check still green. See fixtures/PROVENANCE.md.
#
# Any .blend works in its place; no operation in the chain is specific to this one.
#
# The demonstrations are sibling projects under work/demo/. That is what lets the viewer
# offer both: the neighbourhood a page may switch between is the active project's siblings.
# The repository root keeps no marker, so an ad-hoc command there behaves as it always did.
#
# ponytail: destructive on this demonstration's project, nothing else. Run it by hand.
set -uo pipefail
INSTALL="$(cd "$(dirname "$0")/.." && pwd)"
M="$INSTALL/bin/meshanvil"
ASSET="${1:-$INSTALL/fixtures/demo_car.blend}"
PROJECT="$INSTALL/work/demo/vehicle"

echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"

cp "$ASSET" work/out/demo_car.blend
# scan_defects --fix saves in place, so the pristine source is kept and the repair happens on
# a copy. The copy is byte-identical, which is why 002 has to declare its parent.
cp work/out/demo_car.blend work/out/demo_car_fixed.blend

echo "== 001 what the asset is hiding"
$M run scan_defects work/out/demo_car.blend
echo "== 002 drop the coincident duplicates"
$M run scan_defects work/out/demo_car_fixed.blend --set fix=true --from 001

echo "== 003 bake the stack: fifteen Mirror hold half the car"
$M run apply_modifiers work/out/demo_car_fixed.blend --set max_subsurf_level=1

echo "== 004 what is never visible from outside"
$M run ray_visibility work/out/demo_car_fixed_baked.blend --set grid=48
echo "== 004a back to real size, on the print bed"
$M run recenter work/out/demo_car_fixed_baked.blend --set scale=0.62

echo "== 005 wall every open panel, above the voxel that follows"
$M run solidify work/out/demo_car_fixed_baked_placed.blend --set thickness_mm=20 --set next_voxel_mm=12

# The branch worth reading. Same parent, same voxel, one step apart: the walled body remeshes
# into a solid, the bare panels remesh into shreds and the prune throws the car away. Both
# report every topology check green; only the shell count and the render disagree.
echo "== 006 one closed solid at 12 mm"
$M run voxel_remesh work/out/demo_car_fixed_baked_placed_solid.blend --set voxel_mm=12
echo "== 005a the same remesh without the wall -- the trap"
$M run voxel_remesh work/out/demo_car_fixed_baked_placed.blend --set voxel_mm=12

# A coarse voxel is what someone reaches for to cut the triangle count. The tolerance is the
# honest part: printing at 1:10, 40 mm of drift on the model is 4 mm on the part, so 12 mm is
# declared and the operation enforces it. It fails, and the report keeps the reason.
echo "== 006a a coarser voxel against a real tolerance -- fails, kept"
$M run voxel_remesh work/out/demo_car_fixed_baked_placed_solid.blend --set voxel_mm=40 --set max_bbox_drift_mm=12

echo "== 007 drop what is too small to print"
$M run clean_shells work/out/demo_car_fixed_baked_placed_solid_voxel12.blend
echo "== 008 inventory of what is left"
$M run list_shells work/out/demo_car_fixed_baked_placed_solid_voxel12_cleaned.blend

echo "== viewer"
$M view --no-open

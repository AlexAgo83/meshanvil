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
# ponytail: destructive on work/ops and the demo blends, nothing else. Run it by hand.
set -uo pipefail
cd "$(dirname "$0")/.."

M="bin/meshanvil"
ASSET="${1:-fixtures/demo_car.blend}"

echo "== reset"
rm -rf work/ops
rm -f work/out/demo_car*.blend work/renders/0*_demo_car*.png
mkdir -p work/out

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

echo "== 007 drop what is too small to print"
$M run clean_shells work/out/demo_car_fixed_baked_placed_solid_voxel12.blend
echo "== 008 inventory of what is left"
$M run list_shells work/out/demo_car_fixed_baked_placed_solid_voxel12_cleaned.blend

echo "== viewer"
$M view --no-open

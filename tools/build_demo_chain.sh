#!/usr/bin/env bash
# Rebuild the demo dataset the viewer ships with: one generated scene, then the real
# operations run through the real CLI. Nothing here fabricates a report -- every number
# in work/ops/ comes out of Blender, which is the whole point of the viewer.
#
# ponytail: destructive on work/ops and the demo blends, nothing else. Run it by hand.
set -uo pipefail
cd "$(dirname "$0")/.."

BLENDER="${MESHANVIL_BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
M="bin/meshanvil"

echo "== reset"
rm -rf work/ops
rm -f work/out/demo_source.blend work/out/demo_fixed*.blend work/renders/00*_demo_*.png

echo "== scene"
"$BLENDER" -b -P tools/make_demo_scene.py >/dev/null

# scan_defects --fix saves in place, so the pristine source is kept and the repair
# happens on a copy. The copy is byte-identical, which is why 002 declares its parent.
cp work/out/demo_source.blend work/out/demo_fixed.blend

echo "== 001 inspect the source"
$M run scan_defects work/out/demo_source.blend
echo "== 002 repair the export defects"
$M run scan_defects work/out/demo_fixed.blend --set fix=true --from 001
echo "== 003 outer envelope by ray visibility"
$M run ray_visibility work/out/demo_fixed.blend --set grid=40
echo "== 003a printable envelope, 6 mm voxel"
$M run voxel_remesh work/out/demo_fixed.blend --set voxel_mm=6 --set max_bbox_drift_mm=12
echo "== 003b the 30 mm trap, kept on purpose"
$M run voxel_remesh work/out/demo_fixed.blend --set voxel_mm=30
echo "== 004 drop the small shells"
$M run clean_shells work/out/demo_fixed_voxel6.blend
echo "== 004a enumerate what is left"
$M run list_shells work/out/demo_fixed_voxel6.blend
echo "== 005 sit it on the print bed"
$M run recenter work/out/demo_fixed_voxel6_cleaned.blend

echo "== prune the artefacts no longer reachable"
$M prune --keep 3

echo "== viewer"
$M view --no-open

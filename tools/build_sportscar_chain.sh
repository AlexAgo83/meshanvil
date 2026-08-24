#!/usr/bin/env bash
# Run the real operations over the generated sports car, through the real CLI. Nothing here
# fabricates a report: every number in work/ops/ comes out of Blender.
#
# This subject is the counterpart of build_demo_chain.sh's. That one carries deliberate
# defects so the chain has something to find; this one is meant to come out clean, so the
# chain is what proves it -- scan_defects finding nothing is a result, not a missing step.
#
# ponytail: destructive on this demonstration's project, nothing else. Run it by hand.
set -uo pipefail
INSTALL="$(cd "$(dirname "$0")/.." && pwd)"
M="$INSTALL/bin/meshanvil"
BLENDER="${MESHANVIL_BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
PROJECT="$INSTALL/work/demo/sportscar"

ASSET="${1:-}"
if [ -z "$ASSET" ]; then
  echo "== generating the subject"
  ASSET="$INSTALL/work/out/sportscar.blend"
  "$BLENDER" -b -P "$INSTALL/tools/make_sportscar.py" -- "$ASSET"
fi

echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"
cp "$ASSET" work/out/sportscar.blend

echo "== 001 is the subject clean as generated"
$M run scan_defects work/out/sportscar.blend
echo "== 001a look at it -- the silhouette is judged here, in the chain, not beside it"
$M run render_subject work/out/sportscar.blend

echo "== 002 one shell per part, and how many parts"
$M run list_shells work/out/sportscar.blend
echo "== 003 what a viewer sees from outside"
$M run ray_visibility work/out/sportscar.blend --set grid=64

echo "== 004 to 1:18 on the print bed"
$M run recenter work/out/sportscar.blend --set scale=0.0556
echo "== 005 wall the panels the glasshouse cut open"
$M run solidify work/out/sportscar_placed.blend --set thickness_mm=1.6 --set thickness_clamp=0 --set next_voxel_mm=0.8
echo "== 006 one closed solid"
$M run voxel_remesh work/out/sportscar_placed_solid.blend --set voxel_mm=0.8
echo "== 007 drop what is too small to print"
$M run clean_shells work/out/sportscar_placed_solid_voxel0.8.blend --set min_vertices=200

echo "== done"

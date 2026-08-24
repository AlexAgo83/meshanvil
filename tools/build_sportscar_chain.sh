#!/usr/bin/env bash
# Run the real operations over the generated sports car, through the real CLI. Nothing here
# fabricates a report: every number in work/ops/ comes out of Blender.
#
# This subject is the counterpart of build_demo_chain.sh's. That one carries deliberate
# defects so the chain has something to find; this one is meant to come out clean, so the
# chain is what proves it -- scan_defects finding nothing is a result, not a missing step.
#
# The deliverable is the generated subject itself: 27 objects, one per material group, with
# the topology the generator intended. The printable solid is a *derivative* -- useful, and
# not a better version of the same thing. It costs 2.2k vertices turning into 150k and every
# component boundary along with them, which is what a voxel remesh is for and is exactly
# wrong as a destination for an editable asset. It is therefore opt-in: pass --solid.
# Voir run_012 and run_006.
#
# ponytail: destructive on this demonstration's project, nothing else. Run it by hand.
set -uo pipefail
INSTALL="$(cd "$(dirname "$0")/.." && pwd)"
M="$INSTALL/bin/meshanvil"
BLENDER="${MESHANVIL_BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
PROJECT="$INSTALL/work/demo/sportscar"

SOLID=""
ASSET=""
for arg in "$@"; do
  case "$arg" in
    --solid) SOLID=1 ;;
    *) ASSET="$arg" ;;
  esac
done

echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"

if [ -n "$ASSET" ]; then
  cp "$ASSET" work/out/sportscar.blend
  ASSET=work/out/sportscar.blend
else
  # The subject starts empty: stage 1 has to make the body, not inherit it.
  "$BLENDER" -b --python-expr "
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.save_as_mainfile(filepath='$PROJECT/work/out/sportscar.blend', compress=True)
" >/dev/null 2>&1
  IN=work/out/sportscar.blend
  for STAGE in 1 2 3 4 5; do
    echo "== 00$STAGE build sportscar stage $STAGE"
    $M run make_sportscar "$IN" --set stage=$STAGE || exit 1
    IN=work/out/sportscar_s$STAGE.blend
  done
  ASSET="$IN"
fi

echo "== 006 is the subject clean as generated"
$M run scan_defects "$ASSET"
echo "== 007 look at it -- silhouette is judged here, in the chain, not beside it"
$M run render_subject "$ASSET"
echo "== 008 one shell per part, and how many parts"
$M run list_shells "$ASSET"
echo "== 009 what a viewer sees from outside"
$M run ray_visibility "$ASSET" --set grid=64

if [ -z "$SOLID" ]; then
  echo "== stopping at the editable master. --solid derives the printable branch as well."
  exit 0
fi

# Everything past here is the validation branch. It reads the master and writes new files;
# the master is never touched, which is what makes it a branch rather than a pipeline stage.
echo "== 010 to 1:18 on the print bed"
$M run recenter "$ASSET" --set scale=0.0556
echo "== 011 wall the panels the glasshouse cut open"
$M run solidify work/out/sportscar_placed.blend --set thickness_mm=1.6 --set thickness_clamp=0 --set next_voxel_mm=0.8
echo "== 012 one closed solid -- 27 objects and their boundaries become one mesh here"
$M run voxel_remesh work/out/sportscar_placed_solid.blend --set voxel_mm=0.8
echo "== 013 look at what the remesh cost, against 007"
$M run render_subject work/out/sportscar_placed_solid_voxel0.8.blend

echo "== done"

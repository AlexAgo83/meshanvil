#!/usr/bin/env bash
# The second demonstration: a sound subject, taken to a print size, remeshed twice.
#
# Where the vehicle chain is a list of defects being found, this one is mostly the sweeps
# reporting nothing, and that is the point -- a demonstration where every check fires on
# everything never shows that the checks discriminate.
#
# No donor file is shipped or downloaded: tools/make_demo_figure.py builds a simple standing
# figure from primitives, on the fly, at a real human height with a genuinely thin feature
# (fingers) for the branch below to expose. Every part is an individually closed primitive,
# joined without welding, so the source is sound by construction -- no defect to plant.
#
# The branch at the end is the lesson the vehicle cannot carry. It is remeshed at its real
# size, where a voxel in millimetres and a voxel as a fraction of the subject feel like the
# same number. At a small print size they do not: a voxel that sounds fine turns out to be
# about as wide as a finger. Both runs report ok on every topology and volume check.
#
# A sibling project of the vehicle demonstration, which is what lets the viewer offer both.
#
# ponytail: destructive on this demonstration's project, nothing else. Run it by hand.
set -uo pipefail
INSTALL="$(cd "$(dirname "$0")/.." && pwd)"
M="$INSTALL/bin/meshanvil"
BLENDER="${MESHANVIL_BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
PROJECT="$INSTALL/work/demo/figurine"

ASSET="${1:-}"
if [ -z "$ASSET" ]; then
  echo "== generating a figurine-scale asset (no asset given)"
  ASSET="$INSTALL/work/out/generated_figure.blend"
  "$BLENDER" -b -P "$INSTALL/tools/make_demo_figure.py" -- "$ASSET"
fi

echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"

cp "$ASSET" work/out/figure.blend

echo "== 001 what the sweep finds on a sound subject"
$M run scan_defects work/out/figure.blend

echo "== 002 what is sealed inside it"
$M run ray_visibility work/out/figure.blend --set grid=48

# The subject is authored at a real 1750 mm human height. A generated asset knows its own
# unit, but the decision to shrink it to a figurine is still a decision, and this is where
# it gets recorded: 0.10286 takes it to 180 mm.
echo "== 003 the size decision: 1750 mm to 180 mm"
$M run recenter work/out/figure.blend --set scale=0.10286

# 0.5 mm is a third of the finger; 1.5 mm is close to all of it. Neither is refused, both
# report ok, and only the renders and the thin-feature guard tell them apart.
echo "== 004 remeshed at a third of the thinnest feature"
$M run voxel_remesh work/out/figure_placed.blend --set voxel_mm=0.5 --set max_bbox_drift_mm=1
echo "== 004a the same subject at one voxel across a finger -- the trap"
$M run voxel_remesh work/out/figure_placed.blend --set voxel_mm=1.5 --set max_bbox_drift_mm=3

echo "== 005 what is left"
$M run list_shells work/out/figure_placed_voxel0.5.blend

echo "== viewer"
$M view --no-open

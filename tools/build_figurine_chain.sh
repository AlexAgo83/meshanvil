#!/usr/bin/env bash
# The second demonstration: a sound subject, taken to a print size, remeshed twice.
#
# Where the vehicle chain is a list of defects being found, this one is mostly the sweeps
# reporting nothing, and that is the point -- a demonstration where every check fires on
# everything never shows that the checks discriminate.
#
# The branch at the end is the lesson the vehicle cannot carry. It is remeshed at its real
# size, four metres long, where a voxel in millimetres and a voxel as a fraction of the
# subject feel like the same number. At 180 mm they do not: 1.5 mm sounds fine and is one
# voxel across a finger. Both runs report ok on every topology and volume check.
#
# A sibling project of the vehicle demonstration, which is what lets the viewer offer both.
#
# ponytail: destructive on this demonstration's project, nothing else. Run it by hand.
set -uo pipefail
INSTALL="$(cd "$(dirname "$0")/.." && pwd)"
M="$INSTALL/bin/meshanvil"
ASSET="${1:-$INSTALL/fixtures/demo_figure.blend}"
PROJECT="$INSTALL/work/demo/figurine"

echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"

cp "$ASSET" work/out/figure.blend

echo "== 001 what the sweep finds on a sound subject"
$M run scan_defects work/out/figure.blend

echo "== 002 what is sealed inside it"
$M run ray_visibility work/out/figure.blend --set grid=48

# The subject is authored at 20 741 mm tall, which is not a defect: an interchange file
# declares no unit, so the size is a decision and this is where it gets recorded. 0.00868
# takes it to 180 mm, a figurine.
echo "== 003 the size decision: 20 741 mm to 180 mm"
$M run recenter work/out/figure.blend --set scale=0.00868

# 0.5 mm is a third of the thinnest feature; 1.5 mm is all of it. Neither is refused, both
# report ok, and only the renders and the thin-feature guard tell them apart.
echo "== 004 remeshed at a third of the thinnest feature"
$M run voxel_remesh work/out/figure_placed.blend --set voxel_mm=0.5 --set max_bbox_drift_mm=1
echo "== 004a the same subject at one voxel across a finger -- the trap"
$M run voxel_remesh work/out/figure_placed.blend --set voxel_mm=1.5 --set max_bbox_drift_mm=3

echo "== 005 what is left"
$M run list_shells work/out/figure_placed_voxel0.5.blend

echo "== viewer"
$M view --no-open

#!/usr/bin/env bash
# The second demonstration: a sound subject, taken to a print size, remeshed twice.
#
# Where the vehicle chain is a list of defects being found, this one is mostly the sweeps
# reporting nothing, and that is the point -- a demonstration where every check fires on
# everything never shows that the checks discriminate.
#
# No donor file is shipped: given no argument, this prefers a hand-modelled asset under
# logics/external/modeles-3D/ if one is present locally (that path is gitignored -- a personal
# asset, never committed, never shipped with the repo), and falls back to generating one from
# primitives with tools/make_demo_figure.py otherwise, so a fresh clone always has a sound,
# closed subject with a genuinely thin feature (fingers) for the branch below to expose.
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
LOCAL_ASSET="$INSTALL/logics/external/modeles-3D/base_meshanvil_figurine.blend"

ASSET="${1:-}"
if [ -z "$ASSET" ]; then
  if [ -f "$LOCAL_ASSET" ]; then
    ASSET="$LOCAL_ASSET"
  else
    echo "== generating a figurine-scale asset (no local or given asset)"
    ASSET="$INSTALL/work/out/generated_figure.blend"
    "$BLENDER" -b -P "$INSTALL/tools/make_demo_figure.py" -- "$ASSET"
  fi
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

# Whichever subject this is (the local hand-modelled one, a generated one, or one passed on
# the command line), it is not authored to any particular real-world unit -- the decision to
# shrink it to a 180 mm figurine is still a decision, computed from what op 001 just measured
# rather than a constant sized for one specific asset's own height.
FIGURE_HEIGHT_MM=$(python3 -c "
import json
b = json.load(open('work/ops/001_scan_defects.json'))['measured']['bbox_mm']
print(b['max'][2] - b['min'][2])
")
FIGURE_SCALE=$(python3 -c "print(180 / $FIGURE_HEIGHT_MM)")
echo "== 003 the size decision: ${FIGURE_HEIGHT_MM} mm to 180 mm"
$M run recenter work/out/figure.blend --set scale="$FIGURE_SCALE"

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

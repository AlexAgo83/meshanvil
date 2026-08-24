#!/usr/bin/env bash
# The meshanvil hammer through the real operations. The subject is the editable master and
# the chain says so: inspections only, no remesh, nothing derived. Voir run_012, step 9.
#
# ponytail: destructive on this demonstration's project, nothing else. Run it by hand.
set -uo pipefail
INSTALL="$(cd "$(dirname "$0")/.." && pwd)"
M="$INSTALL/bin/meshanvil"
BLENDER="${MESHANVIL_BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
PROJECT="$INSTALL/work/demo/hammer"

ASSET="${1:-}"
echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"

if [ -n "$ASSET" ]; then
  cp "$ASSET" work/out/hammer.blend
  ASSET=work/out/hammer.blend
else
  # The subject starts empty: stage 1 has to make the head, not inherit it.
  "$BLENDER" -b --python-expr "
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.save_as_mainfile(filepath='$PROJECT/work/out/hammer.blend', compress=True)
" >/dev/null 2>&1
  IN=work/out/hammer.blend
  for STAGE in 1 2 3 4; do
    echo "== 00$STAGE build hammer stage $STAGE"
    $M run make_hammer "$IN" --set stage=$STAGE || exit 1
    IN=work/out/hammer_s$STAGE.blend
  done
  ASSET="$IN"
fi

echo "== 005 is it clean as generated"
$M run scan_defects "$ASSET"
echo "== 006 the hero view and the three orthographics"
$M run render_subject "$ASSET"
echo "== 007 one shell per part"
$M run list_shells "$ASSET"
echo "== done"

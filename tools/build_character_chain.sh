#!/usr/bin/env bash
# The meshanvil T-pose character, modelled in six stages that are six operations.
#
# The workflow is the point. A generator writing six .blend files beside the chain leaves six
# parentless reports -- six chains, no lineage, nothing to step through. Each stage here reads
# what the previous one produced, so the chain links itself and the viewer walks 001 to 006
# with before/after counts and a wipe at every step. Voir run_012, steps 14-15.
#
# ponytail: destructive on this demonstration's project, nothing else. Run it by hand.
set -uo pipefail
INSTALL="$(cd "$(dirname "$0")/.." && pwd)"
M="$INSTALL/bin/meshanvil"
BLENDER="${MESHANVIL_BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
PROJECT="$INSTALL/work/demo/character"

echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"

# The subject starts empty: stage 1 has to make the blockout, not inherit it.
"$BLENDER" -b --python-expr "
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.save_as_mainfile(filepath='$PROJECT/work/out/character.blend', compress=True)
" >/dev/null 2>&1

IN=work/out/character.blend
for STAGE in 1 2 3 4 5 6; do
  echo "== 00$STAGE stage $STAGE"
  $M run make_character "$IN" --set stage=$STAGE || exit 1
  IN=work/out/character_s$STAGE.blend
done

echo "== 007 is the finished master clean"
$M run scan_defects "$IN"
echo "== done"

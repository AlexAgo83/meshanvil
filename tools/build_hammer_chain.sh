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
if [ -z "$ASSET" ]; then
  echo "== generating the subject"
  ASSET="$INSTALL/work/out/hammer.blend"
  "$BLENDER" -b -P "$INSTALL/tools/make_hammer.py" -- "$ASSET"
fi

echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"
cp "$ASSET" work/out/hammer.blend

echo "== 001 is it clean as generated"
$M run scan_defects work/out/hammer.blend
echo "== 002 the hero view and the three orthographics"
$M run render_subject work/out/hammer.blend
echo "== 003 one shell per part"
$M run list_shells work/out/hammer.blend
echo "== done"

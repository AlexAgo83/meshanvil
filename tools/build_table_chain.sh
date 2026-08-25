#!/usr/bin/env bash
# The reference table, modelled from a photograph, down both branches it can leave by.
#
# One plan (tools/table_dimensions.py), two builders: Blender models it as a mesh, FreeCAD
# rebuilds it as B-rep solids and writes STEP. The STEP is then read back through the import
# chain, so the last render in this project comes from the CAD file and not from the mesh --
# which is the only way to see that the two branches still agree.
#
# ponytail: destructive on this demonstration's project, nothing else. Run it by hand.
set -uo pipefail
INSTALL="$(cd "$(dirname "$0")/.." && pwd)"
M="$INSTALL/bin/meshanvil"
PROJECT="$INSTALL/work/demo/table"
REFERENCE="${1:-$INSTALL/fixtures/reference_table.png}"
[ $# -gt 0 ] && shift

echo "== project"
rm -rf "$PROJECT"
$M init "$PROJECT"
cd "$PROJECT"

# The source of this chain is the photograph, so the photograph is what the chain starts from
# and what every report names as its input. No engine reads it -- the proportions were read off
# it by hand -- and both operations declare that rather than implying otherwise.
cp "$REFERENCE" work/in/reference_table.png

echo "== 001 the table as a mesh, from the photograph"
$M run make_table work/in/reference_table.png "$@" || exit 1
echo "== 002 does it read as the photograph"
$M run render_subject work/out/reference_table.blend
echo "== 003 one shell per part"
$M run list_shells work/out/reference_table.blend
echo "== 004 the same table as B-rep solids, written as STEP"
$M run make_table_step work/in/reference_table.png "$@" || exit 1

echo "== 005 read the STEP back, and render what came out of it"
"$INSTALL/tools/build_step_chain.sh" work/out/reference_table.step

echo "== viewer"
$M view --no-open

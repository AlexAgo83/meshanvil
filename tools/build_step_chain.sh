#!/usr/bin/env bash
# A STEP source through to its renders, in the current project.
#
# FreeCAD reads the STEP and tessellates it, but it is not a renderer -- so the import alone
# leaves a report with no view in it. The renders come from the STL it wrote, carried into
# Blender. That is three operations, and the chain links them by fingerprint on its own.
#
# Extra arguments are forwarded to import_step: --set linear_deflection_mm=0.05 and
# --set angular_deflection_deg=10 are the two that decide how fine the tessellation is.
#
# ponytail: three runs, no cleanup, no project reset. It adds to work/ops like any run does.
set -euo pipefail
M="$(cd "$(dirname "$0")/.." && pwd)/bin/meshanvil"

SOURCE="${1:-}"
if [ -z "$SOURCE" ]; then
  echo "usage: $(basename "$0") <file.step> [--set linear_deflection_mm=0.1 ...]" >&2
  exit 2
fi
shift

# The names the operations derive from the source; nothing here chooses them.
STEM="$(basename "${SOURCE%.*}")"
STL="work/out/${STEM}_step.stl"
BLEND="work/out/${STEM}_step_imported.blend"

echo "== 1/3 read the STEP and tessellate it"
$M run import_step "$SOURCE" "$@"
echo "== 2/3 carry the mesh into Blender"
$M run import_mesh "$STL"
echo "== 3/3 the four canonical views and the hero"
$M run render_subject "$BLEND"

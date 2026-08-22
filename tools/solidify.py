"""Give every open surface a wall, so a remesh has a volume to work on.

A render asset models panels as zero-thickness surfaces: a door is one sheet, not a box.
A voxel remesh of a sheet does not produce a solid, it produces shreds -- the body comes out
as hundreds of disconnected fragments and the shell prune then throws them away, leaving the
wheels and the seats. This operation is step 4 of run_006 and skipping it is why.

The wall has to survive the voxel that follows: anything thinner than one voxel is erased,
so a thickness below the next voxel size is refused rather than silently lost.

Runs standalone or under `meshanvil run solidify <file>`.
Voir run_006_turn_a_cad_assembly_into_a_printable_solid.
"""
import bpy, sys
from pathlib import Path


def _reporter():
    """The job carries the repository root; nothing is installed into the engine's interpreter."""
    import sys, json
    from pathlib import Path
    if "--job" not in sys.argv:
        return None, {}
    args = sys.argv[sys.argv.index("--") + 1:]
    job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
    sys.path.insert(0, job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job


REPORT, JOB = _reporter()
PARAMS = (JOB or {}).get("params", {})
THICKNESS = float(PARAMS.get("thickness_mm", 20.0)) / 1000.0
# Declared, not enforced by this operation: it is the voxel the caller intends to remesh at.
# A wall thinner than one voxel is erased by that remesh, so it is refused here instead.
NEXT_VOXEL = float(PARAMS.get("next_voxel_mm", 0.0)) / 1000.0
SKIP_CLOSED = bool(PARAMS.get("skip_closed", True))
OUT = Path(bpy.data.filepath).with_name(Path(bpy.data.filepath).stem + "_solid.blend")


def log(*parts):
    print("[solidify]", *parts)
    sys.stdout.flush()


if NEXT_VOXEL and THICKNESS < NEXT_VOXEL:
    raise SystemExit("thickness %.1f mm is below the declared voxel %.1f mm; the wall would be erased"
                     % (THICKNESS * 1000, NEXT_VOXEL * 1000))

import bmesh
meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
if not meshes:
    raise SystemExit("no mesh in this file")

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.before(reporting.measure_scene())

walled, already_closed = 0, 0
for index, o in enumerate(meshes):
    if REPORT and index % 10 == 0:
        REPORT.progress("walling", 0.1 + 0.7 * index / len(meshes))
    if SKIP_CLOSED:
        bm = bmesh.new(); bm.from_mesh(o.data)
        open_edges = sum(1 for e in bm.edges if len(e.link_faces) != 2)
        bm.free()
        if open_edges == 0:            # already a volume; a wall would only thicken it wrongly
            already_closed += 1
            continue
    modifier = o.modifiers.new("wall", 'SOLIDIFY')
    modifier.thickness = THICKNESS
    modifier.offset = 0.0              # grow both ways, so the outer silhouette barely moves
    modifier.use_even_offset = True
    modifier.use_rim = True
    modifier.use_rim_only = False
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    walled += 1

log("walled %d objects at %.1f mm, %d were already closed" % (walled, THICKNESS * 1000, already_closed))

closed_after = 0
for o in meshes:
    bm = bmesh.new(); bm.from_mesh(o.data)
    if sum(1 for e in bm.edges if len(e.link_faces) != 2) == 0:
        closed_after += 1
    bm.free()
log("closed objects %d / %d" % (closed_after, len(meshes)))

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)

if REPORT:
    REPORT.after(reporting.measure_scene())
    REPORT.report["params"]["walled_objects"] = walled
    REPORT.report["params"]["already_closed"] = already_closed
    REPORT.report["params"]["closed_after"] = closed_after
    REPORT.finding("closure", walled=walled, already_closed=already_closed,
                   closed_after=closed_after, total=len(meshes))
    if closed_after < len(meshes):
        # Solidify cannot close a surface that self-intersects or has a non-manifold seam.
        # Saying so is the point: the remesh that follows will shred exactly these.
        REPORT.warn("some_objects_are_still_open")
    REPORT.cites("run_006_turn_a_cad_assembly_into_a_printable_solid")
    REPORT.output(str(OUT))
    REPORT.write()

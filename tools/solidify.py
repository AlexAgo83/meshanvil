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
    # The package ships with the tool; the project only holds work.
    sys.path.insert(0, job.get("install") or job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job


REPORT, JOB = _reporter()


def _views():
    """Rendering lives in the engine module. The job carries the repository root; a standalone
    run finds it beside this file, so the same script works either way."""
    import sys
    from pathlib import Path
    sys.path.insert(0, (JOB or {}).get("install") or (JOB or {}).get("root")
                    or str(Path(__file__).resolve().parent.parent))
    from meshanvil_engine import views
    return views


views = _views()
PARAMS = (JOB or {}).get("params", {})
THICKNESS = float(PARAMS.get("thickness_mm", 20.0)) / 1000.0
# Declared, not enforced by this operation: it is the voxel the caller intends to remesh at.
# A wall thinner than one voxel is erased by that remesh, so it is refused here instead.
NEXT_VOXEL = float(PARAMS.get("next_voxel_mm", 0.0)) / 1000.0
SKIP_CLOSED = bool(PARAMS.get("skip_closed", True))
# How open a body may be and still count as a volume. A zero test is the wrong question: a
# sculpt with 4 boundary edges out of 29 600 is a solid body with a pinhole, and walling it
# hollows it -- measured at 14 813 vertices becoming 29 626. An open panel sits orders of
# magnitude above this: its boundary is most of its perimeter.
CLOSED_TOLERANCE = float(PARAMS.get("closed_tolerance", 0.01))
# Even thickness divides by the angle at each vertex, so a near-degenerate corner sends the
# offset to infinity: on this asset a 20 mm wall grew spikes 1.4 m long and put geometry
# 913 mm under the print bed. The clamp caps the offset against local edge length.
CLAMP = float(PARAMS.get("thickness_clamp", 1.0))
# A wall grown both ways moves each face of the box by about half its thickness. Anything
# past this is a spike, not a wall.
DRIFT = float(PARAMS.get("max_bbox_drift_mm", 0.0)) or 2.0 * float(PARAMS.get("thickness_mm", 20.0))
RENDER = bool(PARAMS.get("render", True))
OUT = Path(bpy.data.filepath).with_name(Path(bpy.data.filepath).stem + "_solid.blend")
ROOT = Path((JOB or {}).get("root", Path(__file__).resolve().parent.parent))


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

# No before/after pair either: offset 0 grows the wall both ways, so 20 mm on a four-metre
# car leaves the silhouette where it was. The closure count is the evidence, not the render.

def openness(mesh):
    """Boundary edges, non-manifold edges, and the share of the body they represent."""
    bm = bmesh.new()
    bm.from_mesh(mesh)
    boundary = [e for e in bm.edges if len(e.link_faces) == 1]
    tangled = sum(1 for e in bm.edges if len(e.link_faces) > 2)
    total = len(bm.edges)
    bm.free()
    return boundary, tangled, (len(boundary) + tangled) / max(1, total)


def seal(o, boundary_count):
    """Fill the pinholes of a body that is closed but for a few edges.

    A hole fill adds faces, not vertices, so a body that was solid before is solid after and
    the same size. Returns whether it worked -- a fill can leave a seam the solver cannot
    span, and saying so is better than assuming."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    edges = [e for e in bm.edges if len(e.link_faces) == 1]
    if edges:
        bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    left = sum(1 for e in bm.edges if len(e.link_faces) != 2)
    bm.to_mesh(o.data)
    o.data.update()
    bm.free()
    return left == 0


decisions = {"walled": [], "closed": [], "sealed": [], "seal_failed": []}
walled, already_closed = 0, 0
for index, o in enumerate(meshes):
    if REPORT and index % 10 == 0:
        REPORT.progress("walling", 0.1 + 0.7 * index / len(meshes))
    if SKIP_CLOSED:
        boundary, tangled, share = openness(o.data)
        if not boundary and not tangled:
            decisions["closed"].append(o.name)
            already_closed += 1
            continue
        if share <= CLOSED_TOLERANCE:
            # A volume with a pinhole, not a panel. Sealing keeps it solid; walling would
            # turn it into a shell with a cavity the print will never reach.
            key = "sealed" if seal(o, len(boundary)) else "seal_failed"
            decisions[key].append(o.name)
            already_closed += 1
            continue
    modifier = o.modifiers.new("wall", 'SOLIDIFY')
    modifier.thickness = THICKNESS
    modifier.offset = 0.0              # grow both ways, so the outer silhouette barely moves
    # Even thickness is the cause, not a setting to tune: it scales the offset by 1/cos of
    # the vertex angle, which is unbounded at a near-degenerate corner. Off, the extrusion is
    # exactly `thickness` along the normal, so the box can grow by at most that much per face.
    # The wall thins slightly on a sharp fold; a needle 400 mm long is the alternative.
    modifier.use_even_offset = False
    modifier.use_rim = True
    modifier.use_rim_only = False
    if CLAMP and hasattr(modifier, "thickness_clamp"):
        modifier.thickness_clamp = CLAMP
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    decisions["walled"].append(o.name)
    walled += 1

log("walled %d objects at %.1f mm, %d were already closed" % (walled, THICKNESS * 1000, already_closed))

closed_after = 0
for o in meshes:
    bm = bmesh.new(); bm.from_mesh(o.data)
    if sum(1 for e in bm.edges if len(e.link_faces) != 2) == 0:
        closed_after += 1
    bm.free()
log("closed objects %d / %d" % (closed_after, len(meshes)))

if RENDER:
    views.shoot(REPORT, JOB, ROOT, OUT.stem)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)

if REPORT:
    REPORT.after(reporting.measure_scene())
    REPORT.report["params"]["walled_objects"] = walled
    REPORT.report["params"]["already_closed"] = already_closed
    REPORT.report["params"]["closed_after"] = closed_after
    REPORT.finding("closure", walled=walled, already_closed=already_closed,
                   closed_after=closed_after, total=len(meshes))
    # Which rule applied to which body. `walled 1` was true and told a reader nothing about
    # the decision being wrong; the decision itself is the thing worth recording.
    REPORT.finding("walling_decisions",
                   **{key: len(names) for key, names in decisions.items()},
                   tolerance=CLOSED_TOLERANCE,
                   examples={key: names[:6] for key, names in decisions.items() if names})
    REPORT.report["params"]["walling_decisions"] = {k: len(v) for k, v in decisions.items()}
    if decisions["seal_failed"]:
        REPORT.warn("pinholes_left_open")
    if closed_after < len(meshes):
        # Solidify cannot close a surface that self-intersects or has a non-manifold seam.
        # Saying so is the point: the remesh that follows will shred exactly these.
        REPORT.warn("some_objects_are_still_open")
    # The bounding box is the check that catches this. Every topology count stayed green
    # while the wall was throwing 1.4 m needles off the bodywork; only the box said so.
    box_before = REPORT.report["before"]["bbox_mm"]
    box_after = REPORT.report["after"]["bbox_mm"]
    moved = max(max(abs(box_after["min"][i] - box_before["min"][i]),
                    abs(box_after["max"][i] - box_before["max"][i])) for i in range(3))
    REPORT.report["params"]["bbox_drift_mm"] = round(moved, 3)
    if moved > DRIFT:
        REPORT.warn("wall_grew_spikes")
        REPORT.failed("the wall moved the bounding box by %.1f mm, tolerance is %.1f mm"
                      % (moved, DRIFT))
    REPORT.cites("run_006_turn_a_cad_assembly_into_a_printable_solid")
    REPORT.output(str(OUT))
    REPORT.write()

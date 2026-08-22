"""Bake every modifier into the mesh, so what the file says is what the file has.

A render asset keeps half its geometry in the stack: a Mirror is not geometry until it is
applied, and `join()` drops it without a word. Every downstream operation here joins, so a
chain that skips this step silently remeshes half a car and every topology check still
passes. That is the failure this operation exists to make visible: the vertex count before
and after is the evidence.

Runs standalone or under `meshanvil run apply_modifiers <file>`.
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


def _views():
    """Rendering lives in the engine module. The job carries the repository root; a standalone
    run finds it beside this file, so the same script works either way."""
    import sys
    from pathlib import Path
    sys.path.insert(0, (JOB or {}).get("root") or str(Path(__file__).resolve().parent.parent))
    from meshanvil_engine import views
    return views


views = _views()
PARAMS = (JOB or {}).get("params", {})
# A subdivision cage is cheap; its evaluated mesh is not. Capping the level keeps a 7x
# multiplier from becoming a 30x one on a file nobody sized for printing.
MAX_SUBSURF = int(PARAMS.get("max_subsurf_level", 2))
APPLY_SCALE = bool(PARAMS.get("apply_scale", True))
RENDER = bool(PARAMS.get("render", True))
OUT = Path(bpy.data.filepath).with_name(Path(bpy.data.filepath).stem + "_baked.blend")
ROOT = Path((JOB or {}).get("root", Path(__file__).resolve().parent.parent))


def log(*parts):
    print("[bake]", *parts)
    sys.stdout.flush()


meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
if not meshes:
    raise SystemExit("no mesh in this file")

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.before(reporting.measure_scene())

kinds, capped = {}, 0
for o in meshes:
    for m in o.modifiers:
        kinds[m.type] = kinds.get(m.type, 0) + 1
        if m.type == 'SUBSURF' and m.levels > MAX_SUBSURF:
            m.levels = MAX_SUBSURF
            capped += 1
log("objects %d | modifiers %s | subsurf capped to %d on %d" % (len(meshes), kinds, MAX_SUBSURF, capped))

# No before/after pair here, and the reason is worth keeping: Blender renders the evaluated
# mesh, so an unapplied Mirror is already in the picture. The two sides would be the same
# image while the vertex count doubles. This defect is only visible as a number, which is
# exactly what the docstring above claims.

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = meshes[0]

failed = []
for index, o in enumerate(meshes):
    if REPORT and index % 10 == 0:
        REPORT.progress("baking", 0.1 + 0.7 * index / len(meshes))
    bpy.context.view_layer.objects.active = o
    for m in list(o.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=m.name)
        except RuntimeError as error:      # a disabled or invalid modifier, not a crash
            # The name has to be read before the modifier is dropped: reading it afterwards
            # raises ReferenceError on the removed StructRNA, which escapes, kills Blender
            # and leaves the runner reporting that the engine wrote no report at all.
            name = m.name
            failed.append(f"{o.name}:{name}")
            o.modifiers.remove(m)
            log("could not apply %s on %s (%s)" % (name, o.name, error))

if APPLY_SCALE:
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

left = sum(len(o.modifiers) for o in meshes)
log("modifiers left %d | vertices now %d" % (left, sum(len(o.data.vertices) for o in meshes)))

if RENDER:
    views.shoot(REPORT, JOB, ROOT, OUT.stem)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)

if REPORT:
    REPORT.after(reporting.measure_scene())
    REPORT.report["params"]["modifiers_found"] = kinds
    REPORT.report["params"]["subsurf_capped"] = capped
    if failed:
        REPORT.finding("modifier_not_applied", count=len(failed), which=failed[:12])
        REPORT.warn("some_modifiers_were_dropped")
    if left:
        REPORT.warn("modifiers_remain_after_bake")
    # Baking must not move the outer extent: a Mirror adds geometry inside the existing
    # bounds, a Subsurf shrinks toward the cage. A box that grew means a modifier was
    # doing something other than describing the same object.
    before, after = REPORT.report["before"]["bbox_mm"], REPORT.report["after"]["bbox_mm"]
    grew = [round((after["max"][i] - after["min"][i]) - (before["max"][i] - before["min"][i]), 3)
            for i in range(3)]
    REPORT.report["params"]["size_change_mm"] = grew
    if max(grew) > 1.0:
        REPORT.warn("bbox_grew_while_baking")
    REPORT.cites("run_006_turn_a_cad_assembly_into_a_printable_solid")
    REPORT.output(str(OUT))
    REPORT.write()

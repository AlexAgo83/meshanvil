"""Centre the geometry on X and Y and sit it on z = 0, optionally at a scale.

Runs standalone or under `meshanvil run recenter <file>`.
Voir run_006_turn_a_cad_assembly_into_a_printable_solid.
"""
import bpy, sys, json
from pathlib import Path
from mathutils import Vector
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
SCALE = float(PARAMS.get("scale", 1.0))
OUT = Path(bpy.data.filepath).with_name(Path(bpy.data.filepath).stem + "_placed.blend")


def bounds(objects):
    points = [o.matrix_world @ v.co for o in objects for v in o.data.vertices]
    return (Vector([min(p[i] for p in points) for i in range(3)]),
            Vector([max(p[i] for p in points) for i in range(3)]))


meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
if not meshes:
    raise SystemExit("no mesh in this file")
if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.before(reporting.measure_scene())

low, high = bounds(meshes)
print("[place] before %.1f %.1f %.1f -> %.1f %.1f %.1f mm"
      % (*(low * 1000), *(high * 1000)))

bpy.ops.object.select_all(action='DESELECT')
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if SCALE != 1.0:
    bpy.ops.transform.resize(value=(SCALE, SCALE, SCALE))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    low, high = bounds(meshes)

shift = Vector((-(low.x + high.x) / 2, -(low.y + high.y) / 2, -low.z))
for o in meshes:
    o.location += shift
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

low, high = bounds(meshes)
size = [(high[i] - low[i]) * 1000 for i in range(3)]
print("[place] after  %.1f %.1f %.1f -> %.1f %.1f %.1f mm | %.1f x %.1f x %.1f"
      % (*(low * 1000), *(high * 1000), *size))

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
if REPORT:
    REPORT.after(reporting.measure_scene())
    # Centring moves every axis by construction: what would be wrong is the size changing
    # when no scale was asked for.
    before, after = REPORT.report["before"]["bbox_mm"], REPORT.report["after"]["bbox_mm"]
    grew = [round((after["max"][i] - after["min"][i]) - (before["max"][i] - before["min"][i]), 3)
            for i in range(3)]
    REPORT.report["params"]["size_change_mm"] = grew
    if SCALE == 1.0 and max(abs(v) for v in grew) > 0.01:
        REPORT.warn("size_changed_without_scale")
        REPORT.failed("centring changed the size by %s mm" % grew)
    REPORT.cites("run_006_turn_a_cad_assembly_into_a_printable_solid")
    REPORT.output(str(OUT))
    REPORT.write()

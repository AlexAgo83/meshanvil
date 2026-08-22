"""Drop every shell smaller than a threshold: after any boolean, debris is left behind.

Prunes by size, never by rank -- keeping only the largest shell is what deleted every detached
appendage on the delivered chain. Voir run_006 and run_008.
"""
import bpy, bmesh, sys, json
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
FLOOR = int(PARAMS.get("min_vertices", 3000))
TARGET = PARAMS.get("object") or None
RENDER = bool(PARAMS.get("render", True))
OUT = Path(bpy.data.filepath).with_name(Path(bpy.data.filepath).stem + "_cleaned.blend")
ROOT = Path((JOB or {}).get("root", Path(__file__).resolve().parent.parent))

meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
target = bpy.data.objects[TARGET] if TARGET else max(meshes, key=lambda o: len(o.data.vertices))
if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.before(reporting.measure_object(target.name))

mesh = bmesh.new()
mesh.from_mesh(target.data)
seen, shells = set(), []
for start in mesh.verts:
    if start in seen:
        continue
    stack, shell = [start], []
    seen.add(start)
    while stack:
        vertex = stack.pop()
        shell.append(vertex)
        for edge in vertex.link_edges:
            other = edge.other_vert(vertex)
            if other not in seen:
                seen.add(other)
                stack.append(other)
    shells.append(shell)
shells.sort(key=len, reverse=True)
dropped = [v for shell in shells if len(shell) < FLOOR for v in shell]
kept = sum(1 for shell in shells if len(shell) >= FLOOR)
print("[clean] shells %d | kept %d | dropped %d vertices (floor %d)"
      % (len(shells), kept, len(dropped), FLOOR))
if dropped:
    bmesh.ops.delete(mesh, geom=dropped, context='VERTS')
mesh.to_mesh(target.data)
target.data.update()
mesh.free()

if RENDER:
    views.shoot(REPORT, JOB, ROOT, OUT.stem)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
if REPORT:
    REPORT.after(reporting.measure_object(target.name))
    REPORT.report["params"]["object"] = target.name
    REPORT.report["params"]["shells_before"] = len(shells)
    REPORT.report["params"]["shells_dropped"] = len(shells) - kept
    if kept == 0:
        REPORT.failed("the floor of %d vertices dropped every shell" % FLOOR)
    # Pruning debris must not move the outer extent: if it does, something structural went.
    delta = REPORT.report.get("bbox_delta_mm") or {"axes_moved": []}
    if delta["axes_moved"]:
        REPORT.warn("bbox_moved_while_pruning_debris")
    REPORT.cites("run_008_weld_and_clean_disconnected_shells_in_a_printable_model")
    REPORT.output(str(OUT))
    REPORT.write()

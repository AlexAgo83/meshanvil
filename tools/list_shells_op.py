"""Enumerate the shells of an object: how many, how big, and where each one sits.

The check to run after any boolean, before anything downstream trusts the result.
Voir run_008_weld_and_clean_disconnected_shells_in_a_printable_model.
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
    # The package ships with the tool; the project only holds work.
    sys.path.insert(0, job.get("install") or job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job

REPORT, JOB = _reporter()
PARAMS = (JOB or {}).get("params", {})
TOP = int(PARAMS.get("top", 25))
TARGET = PARAMS.get("object") or None

meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
target = bpy.data.objects[TARGET] if TARGET else max(meshes, key=lambda o: len(o.data.vertices))
world = target.matrix_world
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
print("[shells] %s: %d shells" % (target.name, len(shells)))
for shell in shells[:TOP]:
    points = [world @ v.co for v in shell]
    low = [min(p[i] for p in points) * 1000 for i in range(3)]
    high = [max(p[i] for p in points) * 1000 for i in range(3)]
    print("  %7d v  %.0f x %.0f x %.0f mm"
          % (len(shell), high[0] - low[0], high[1] - low[1], high[2] - low[2]))
small = [s for s in shells[1:] if len(s) < 200]
print("[shells] under 200 vertices: %d" % len(small))
mesh.free()

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.measured(reporting.measure_object(target.name))
    REPORT.report["params"]["object"] = target.name
    REPORT.finding("shells", count=len(shells), largest=len(shells[0]),
                   under_200_vertices=len(small))
    if len(shells) > 1:
        REPORT.finding("debris_candidates", count=len(small),
                       sizes=[len(s) for s in shells[1:6]])
    REPORT.cites("run_008_weld_and_clean_disconnected_shells_in_a_printable_model")
    REPORT.write()

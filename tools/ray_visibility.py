"""Sort objects by whether anything sees them from outside, by firing parallel rays.

The long one: 508 200 rays took about fifteen minutes on a 5.4 M vertex assembly, which is
why it reports progress. Runs standalone or under `meshanvil run ray_visibility <file>`.
Voir run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility.
"""
import bpy, sys, json, math
from pathlib import Path
from mathutils import Vector


def _reporter():
    if "--job" not in sys.argv:
        return None, {}
    args = sys.argv[sys.argv.index("--") + 1:]
    job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
    sys.path.insert(0, job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job


REPORT, JOB = _reporter()
PARAMS = (JOB or {}).get("params", {})
DIRECTIONS = int(PARAMS.get("directions", 42))
GRID = int(PARAMS.get("grid", 110))
CACHE = Path(bpy.data.filepath).parent.parent / "cache" / (
    Path(bpy.data.filepath).stem + "_visibility.json")


def fibonacci(count):
    angle = math.pi * (3 - math.sqrt(5))
    for index in range(count):
        z = 1 - 2 * (index + 0.5) / count
        radius = math.sqrt(max(0.0, 1 - z * z))
        yield Vector((radius * math.cos(angle * index), radius * math.sin(angle * index), z))


meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
points = [o.matrix_world @ Vector(corner) for o in meshes for corner in o.bound_box]
low = Vector([min(p[i] for p in points) for i in range(3)])
high = Vector([max(p[i] for p in points) for i in range(3)])
centre, reach = (low + high) / 2, (high - low).length

graph = bpy.context.evaluated_depsgraph_get()
scene = bpy.context.scene
seen, fired = {}, 0
for index, direction in enumerate(fibonacci(DIRECTIONS)):
    direction.normalize()
    up = Vector((0, 0, 1)) if abs(direction.z) < 0.9 else Vector((1, 0, 0))
    across = direction.cross(up).normalized()
    down = direction.cross(across).normalized()
    half = reach / 2 * 1.05
    for i in range(GRID):
        a = (i + 0.5) / GRID * 2 - 1
        for j in range(GRID):
            b = (j + 0.5) / GRID * 2 - 1
            origin = centre + direction * (reach * 0.75) + across * (a * half) + down * (b * half)
            hit, _, _, _, obj, _ = scene.ray_cast(graph, origin, -direction, distance=reach * 2)
            fired += 1
            if hit and obj is not None:
                seen[obj.name] = seen.get(obj.name, 0) + 1
    if REPORT:
        REPORT.progress(f"direction {index + 1}/{DIRECTIONS}", (index + 1) / DIRECTIONS)
    else:
        print("  direction %2d/%d  objets vus: %d" % (index + 1, DIRECTIONS, len(seen)))

never = sorted({o.name for o in meshes} - set(seen))
faint = [name for name, hits in seen.items() if hits <= 3]
print("=== rayons tires: %d" % fired)
print("=== meshes: %d | vus: %d | jamais vus: %d" % (len(meshes), len(seen), len(never)))
CACHE.parent.mkdir(parents=True, exist_ok=True)
CACHE.write_text(json.dumps({"seen": seen, "never": never, "rays": fired}, indent=1) + "\n",
                 encoding="utf-8")

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.measured(reporting.measure_scene())
    REPORT.report["params"]["rays"] = fired
    REPORT.finding("visibility", seen=len(seen), never_seen=len(never),
                   faint=len(faint), cache=str(CACHE))
    if never:
        REPORT.finding("never_seen_objects", count=len(never), examples=never[:5])
    # A thin part falls through the grid and comes out "never seen" although it is visible.
    REPORT.warn("thin_parts_below_ray_grid")
    REPORT.cites("run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility")
    REPORT.write()

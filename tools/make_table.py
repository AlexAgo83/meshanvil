"""Generate the reference coffee table: two rounded slabs on four splayed tapered legs.

The subject is a photograph, and a photograph is a silhouette and nothing else -- it carries
no dimension. So the proportions are read off the image and the sizes are declared as
parameters: 1100 x 600 x 400 mm is a coffee table, not a measurement of *that* coffee table.
Anyone who has the real one measures it and passes the numbers.

What the image does decide, and what the numbers cannot: the corners of both slabs are
rounded, the legs are round and taper toward the floor, and they splay outward in both
directions. That splay is the whole character of the piece -- vertical legs turn it into a
box on stilts.

    blender -b -P tools/make_table.py -- <destination.blend>
"""
import bpy, bmesh, json, os, sys
from pathlib import Path
from mathutils import Vector


def _reporter():
    if "--job" not in sys.argv:
        return None, {}
    args = sys.argv[sys.argv.index("--") + 1:]
    job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
    sys.path.insert(0, job.get("install") or job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job


REPORT, JOB = _reporter()
PARAMS = (JOB or {}).get("params", {})

SOURCE = Path((JOB or {}).get("target", ""))
INSTALL = (JOB or {}).get("install") or str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, INSTALL)
from tools import table_dimensions

MM = 0.001                              # the plan is in millimetres, the scene is in metres
PLAN = table_dimensions.layout(
    length=float(PARAMS.get("length_mm", table_dimensions.LENGTH)),
    width=float(PARAMS.get("width_mm", table_dimensions.WIDTH)),
    height=float(PARAMS.get("height_mm", table_dimensions.HEIGHT)),
    shelf_fraction=float(PARAMS.get("shelf_fraction", table_dimensions.SHELF_FRACTION)))
EASE = PLAN["ease"] * MM

OAK = (0.72, 0.55, 0.34, 1)


def material():
    wood = bpy.data.materials.get("oak") or bpy.data.materials.new("oak")
    wood.diffuse_color = OAK
    return wood


def slab(name, size_x, size_y, thick, top_z, corner):
    """A rounded rectangle with eased edges, hung under `top_z`.

    Two bevels, not one: the corner radius and the edge softening differ by a factor of
    twenty, and a single bevel that rounds the corners also eats the whole thickness.
    """
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for vert in bm.verts:
        vert.co = Vector((vert.co.x * size_x, vert.co.y * size_y, vert.co.z * thick))
    upright = [e for e in bm.edges if e.verts[0].co.z != e.verts[1].co.z]
    bmesh.ops.bevel(bm, geom=upright, offset=corner, segments=10,
                    affect='EDGES', profile=0.5, clamp_overlap=True)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=EASE, segments=3,
                    affect='EDGES', profile=0.5, clamp_overlap=True)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, top_z - thick / 2)))
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material())
    return obj


def leg(name, shoulder, foot):
    """One tapered leg, built between the two points that matter: where it meets the top and
    where it stands. Given the points, the lean is a consequence and not a second guess."""
    down = foot - shoulder
    bpy.ops.mesh.primitive_cone_add(vertices=28, radius1=PLAN["leg_top"] * MM,
                                    radius2=PLAN["leg_foot"] * MM,
                                    depth=down.length, location=(shoulder + foot) / 2)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = down.to_track_quat('Z', 'Y')
    obj.data.materials.append(material())
    return obj


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    slab("top", PLAN["length"] * MM, PLAN["width"] * MM, PLAN["top_thick"] * MM,
         PLAN["height"] * MM, PLAN["corner"] * MM)
    slab("shelf", PLAN["shelf_x"] * MM, PLAN["shelf_y"] * MM, PLAN["shelf_thick"] * MM,
         PLAN["shelf_z"] * MM, PLAN["shelf_corner"] * MM)
    for index, (shoulder, foot) in enumerate(PLAN["legs"]):
        leg("leg_%d" % index, Vector(shoulder) * MM, Vector(foot) * MM)


def save(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    return path


build()

if REPORT:
    from meshanvil_engine import report as reporting
    out = Path(JOB["root"]) / "work" / "out" / (Path(JOB["target"]).stem + ".blend")
    save(str(out))
    measured = reporting.measure_scene()
    REPORT.measured(measured)
    REPORT.report["params"]["parts"] = 6
    REPORT.finding("built", objects=measured["objects"], vertices=measured["vertices"],
                   length_mm=round(PLAN["length"]), width_mm=round(PLAN["width"]),
                   height_mm=round(PLAN["height"]))
    # The photograph is the source and it is declared as one, but no engine reads a photograph:
    # the proportions were read off it by hand into tools/table_dimensions.py, and the only
    # check that the model still matches it is a person looking at the render.
    REPORT.warn("target_not_read")
    REPORT.warn("not_compared_to_reference_image")
    # The reference belongs in the preview beside the renders: the comparison this operation
    # cannot make is the one a person makes by looking, and they should not have to go and
    # find the file to make it. It is the source, and the camera field says so.
    REPORT.render("reference", str(SOURCE), "photograph, not a render")
    REPORT.output(str(out))
    REPORT.write()
else:
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    target = next((a for a in args if not a.startswith("--")), None) or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "out", "table.blend")
    print("[make_table]", save(target))

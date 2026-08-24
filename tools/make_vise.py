"""Build the meshanvil bench vise one stage at a time, as operations rather than as a script.

The point of this file is as much the workflow as the vise. A generator that writes six .blend
files beside the chain produces six parentless reports -- six chains, no lineage, nothing to
step through. Modelled as a transform whose input is the previous stage's output, the chain
links itself: each stage carries before/after counts, its own renders, and a wipe against the
state before it. That is a reusable shape for any staged generation, not a fixture for this
subject. Voir run_012, step 14.

    meshanvil run make_vise <file.blend> --set stage=N

Style is read off viewer/icon.png, as the hammer's is: faceted low-poly, graphite, with the
accent copper (#ed9e5c) on the surfaces that do the work.
"""
import bpy, bmesh, sys, json, math, re
from pathlib import Path


def _reporter():
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
    sys.path.insert(0, (JOB or {}).get("install") or (JOB or {}).get("root")
                    or str(Path(__file__).resolve().parent.parent))
    from meshanvil_engine import views
    return views


views = _views()
PARAMS = (JOB or {}).get("params", {})
STAGE = int(PARAMS.get("stage", 1))
RENDER = bool(PARAMS.get("render", True))
ROOT = Path((JOB or {}).get("root", Path(__file__).resolve().parent.parent))
MM = 0.001

STAGE_NAMES = {1: "Blockout", 2: "Mechanical structure", 3: "Functional details",
               4: "Refined shape", 5: "Secondary details", 6: "Materials"}

MATERIALS = {
    "body": (0.22, 0.235, 0.26, 1),      # painted cast iron
    "base": (0.20, 0.215, 0.24, 1),
    "jaw": (0.26, 0.275, 0.30, 1),
    "plate": (0.93, 0.62, 0.36, 1),      # #ed9e5c: the jaws are what does the work
    "screw": (0.46, 0.47, 0.50, 1),      # bright steel
    "rail": (0.40, 0.41, 0.44, 1),
    "handle": (0.13, 0.13, 0.15, 1),
    "bolt": (0.55, 0.56, 0.58, 1),
}

# --- geometry helpers ------------------------------------------------------------------

def new_object(name, mesh):
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(ob)
    return ob


def octagon(half_a, half_b, chamfer=0.28):
    """A rectangle with its corners cut: the section everything here is swept from, and the
    facet the icon is drawn in."""
    a, b, c = half_a, half_b, chamfer
    return [(a, b * (1 - c)), (a * (1 - c), b), (-a * (1 - c), b), (-a, b * (1 - c)),
            (-a, -b * (1 - c)), (-a * (1 - c), -b), (a * (1 - c), -b), (a, -b * (1 - c))]


def loft(rings, name):
    """Bridge rings into quads and cap both ends: one closed shell."""
    bm = bmesh.new()
    loops = [[bm.verts.new(p) for p in r] for r in rings]
    bm.verts.ensure_lookup_table()
    for a, b in zip(loops, loops[1:]):
        for i in range(len(a)):
            j = (i + 1) % len(a)
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(list(reversed(loops[0])))
    bm.faces.new(loops[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return new_object(name, mesh)


def block(name, x, y, z, chamfer=0.0):
    """A box, optionally with its vertical corners cut, swept along X."""
    (x0, x1), (y0, y1), (z0, z1) = x, y, z
    cy, cz = (y0 + y1) / 2, (z0 + z1) / 2
    hb, hc = (y1 - y0) / 2, (z1 - z0) / 2
    section = octagon(hb, hc, chamfer) if chamfer else [(hb, hc), (-hb, hc), (-hb, -hc), (hb, -hc)]
    rings = [[(v * MM, (cy + a) * MM, (cz + b) * MM) for a, b in section] for v in (x0, x1)]
    return loft(rings, name)


def bar(name, axis, span, radius, centre, segments=12):
    """A prism along one axis: the screw, the rail and the handle are all this."""
    a0, a1 = span
    rings = []
    for value in (a0, a1):
        ring = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            u, v = radius * math.cos(angle), radius * math.sin(angle)
            point = {"x": (value, centre[1] + u, centre[2] + v),
                     "y": (centre[0] + u, value, centre[2] + v),
                     "z": (centre[0] + u, centre[1] + v, value)}[axis]
            ring.append(tuple(c * MM for c in point))
        rings.append(ring)
    return loft(rings, name)


def cut(target, tool):
    """Subtract one object from another and drop the tool. Booleans on chunky, closed,
    axis-aligned shapes are the reliable case; scan_defects in the chain says whether it
    stayed that way, which is the reason to do this inside the chain rather than beside it."""
    modifier = target.modifiers.new("cut", 'BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = tool
    modifier.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(tool, do_unlink=True)


def bevel_all(ob, width):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.bevel(bm, geom=bm.verts[:] + bm.edges[:], offset=width * MM, segments=1,
                    affect='EDGES', clamp_overlap=True)
    bm.to_mesh(ob.data)
    bm.free()


def taper(ob, z_low, z_high, shrink):
    """Pull the top of a part in toward its own vertical axis. This is what stops a casting
    reading as an extruded box, and it is a real edit of the geometry the blockout left --
    not a replacement of it."""
    centre_x = sum(v.co.x for v in ob.data.vertices) / len(ob.data.vertices)
    centre_y = sum(v.co.y for v in ob.data.vertices) / len(ob.data.vertices)
    for v in ob.data.vertices:
        t = (v.co.z / MM - z_low) / max(z_high - z_low, 1e-6)
        t = min(max(t, 0.0), 1.0)
        factor = 1 - shrink * t
        v.co.x = centre_x + (v.co.x - centre_x) * factor
        v.co.y = centre_y + (v.co.y - centre_y) * factor


def find(name):
    return bpy.data.objects.get(name)


# --- stages ----------------------------------------------------------------------------

def stage_1_blockout():
    """Primary volumes only. Proportions are decided here and nowhere else."""
    # Parts sit on each other, never inside each other. The first layout had the fixed jaw
    # embedded in the body over its whole height, which reads as one lump and is exactly the
    # gross intersection this is meant to avoid.
    block("base", (-150, 70), (-78, 78), (0, 22))
    block("body", (-150, -58), (-48, 48), (22, 94))
    block("jaw_fixed", (-104, -58), (-52, 52), (94, 152))
    block("jaw_sliding", (-12, 44), (-52, 52), (40, 152))


def stage_2_mechanical():
    """The mechanism: what the sliding jaw rides on and what drives it."""
    block("rail", (-58, 118), (-22, 22), (40, 74))
    bar("screw", "x", (-40, 142), 11, (0, 0, 57))
    block("screw_housing", (44, 84), (-28, 28), (34, 82), chamfer=0.32)


def stage_3_functional():
    """What a hand touches, and what the vise is bolted down by."""
    bar("handle", "y", (-88, 88), 8, (128, 0, 57))
    for side, y in (("a", -88), ("b", 88)):
        bar(f"handle_stop_{side}", "y", (y - 14 if y < 0 else y, y if y < 0 else y + 14),
            13, (128, 0, 57))
    # The plates stand proud of the jaw faces they bolt to: a plate flush with its jaw is a
    # painted rectangle, and a plate sunk into it is not a replaceable part.
    block("plate_fixed", (-58, -48), (-46, 46), (98, 146), chamfer=0.18)
    block("plate_moving", (-12, -2), (-46, 46), (98, 146), chamfer=0.18)
    # Mounting holes: real holes, cut out of the base rather than suggested by a dark disc.
    base = find("base")
    # Clear of the casting foot: holes under it are holes nobody can reach a spanner into,
    # and in plan they simply did not read.
    for x, y in ((-128, -64), (-128, 64), (40, -64), (40, 64)):
        cut(base, bar(f"hole_{x}_{y}", "z", (-6, 30), 8, (x, y, 0)))


def stage_4_refine():
    """Tapers and chamfers over the blockout: the same parts, no longer extruded boxes."""
    for name, low, high, shrink in (("body", 24, 96, 0.16), ("jaw_fixed", 24, 150, 0.13),
                                    ("jaw_sliding", 24, 150, 0.13), ("base", 0, 24, 0.06)):
        ob = find(name)
        if ob:
            taper(ob, low, high, shrink)
    for ob in (o for o in bpy.data.objects if o.type == 'MESH'):
        bevel_all(ob, 2.4 if ob.name in ("base", "body", "jaw_fixed", "jaw_sliding") else 1.2)


def stage_5_secondary():
    """Restrained industrial detail: what fastens the plates, and where the casting steps."""
    for label, x in (("fixed", -53), ("moving", -7)):
        for z in (110, 136):
            bar(f"bolt_{label}_{z}", "x", (x - 7, x + 7), 6, (0, 0, z))
    # A foot under the casting and a rib along its flank: the two places a cast body actually
    # steps. A skirt run around the whole base read as a second plate stacked under the first.
    block("body_foot", (-150, -58), (-50, 50), (22, 32), chamfer=0.30)
    block("body_rib", (-142, -66), (-14, 14), (86, 96), chamfer=0.34)


def stage_6_materials():
    """One material per functional group, assigned by name prefix so the object's own name is
    the single source of truth about what it is."""
    for ob in (o for o in bpy.data.objects if o.type == 'MESH'):
        group = next((k for k in MATERIALS if ob.name.startswith(k)), "body")
        if ob.name.startswith("jaw"):
            group = "jaw"
        if ob.name.startswith("plate"):
            group = "plate"
        material = bpy.data.materials.get(group)
        if material is None:
            material = bpy.data.materials.new(group)
            material.diffuse_color = MATERIALS[group]
            material.use_nodes = False
        ob.data.materials.clear()
        ob.data.materials.append(material)
        ob.color = MATERIALS[group]


STAGES = {1: stage_1_blockout, 2: stage_2_mechanical, 3: stage_3_functional,
          4: stage_4_refine, 5: stage_5_secondary, 6: stage_6_materials}

if STAGE not in STAGES:
    message = f"no stage {STAGE}: this vise has {len(STAGES)}"
    if REPORT:
        REPORT.failed(message)
        REPORT.write()
    sys.exit(message)

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.before(reporting.measure_scene())

STAGES[STAGE]()

# Strip any stage suffix the input already carries, so six stages give vise_s1 .. vise_s6
# rather than vise_s1_s2_s3_s4_s5_s6.
source = Path(bpy.data.filepath)
OUT = source.with_name(f"{re.sub(r'(_s[0-9]+)+$', '', source.stem)}_s{STAGE}.blend")

if RENDER:
    views.shoot(REPORT, JOB, ROOT, OUT.stem)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
open_edges = 0
for o in meshes:
    bm = bmesh.new(); bm.from_mesh(o.data)
    open_edges += sum(1 for e in bm.edges if len(e.link_faces) != 2)
    bm.free()
print("[make_vise] stage %d %s: %d objects, %d open edges"
      % (STAGE, STAGE_NAMES[STAGE], len(meshes), open_edges))

if REPORT:
    REPORT.after(reporting.measure_scene())
    REPORT.report["params"]["stage_name"] = "%02d %s" % (STAGE, STAGE_NAMES[STAGE])
    REPORT.report["params"]["objects"] = len(meshes)
    REPORT.finding("stage", number=STAGE, name=STAGE_NAMES[STAGE], objects=len(meshes),
                   open_edges=open_edges)
    if open_edges:
        REPORT.warn("stage_left_open_edges")
    REPORT.cites("run_012_build_a_recognizable_low_poly_subject_from_primitives")
    REPORT.output(str(OUT))
    REPORT.write()

"""Generate a sports-car subject from primitives -- no donor file, nothing to license.

The third generated subject in this project, and the first meant to come out *clean*:
make_demo_vehicle.py carries deliberate defects because the demonstration chain needs
something to find. This one is the opposite -- closed shells, symmetry by construction,
wheels on the ground, one object per material group -- so it can be edited or printed
rather than repaired.

Authored in millimetres at true scale: 4450 x 1900 x 1250, wheelbase 2650, wheel 678.

    blender -b -P tools/make_sportscar.py -- <destination.blend> [--preview]
"""
import bpy, bmesh, os, sys, math
from mathutils import Vector

MM = 0.001
LENGTH, WIDTH, HEIGHT = 4450 * MM, 1900 * MM, 1250 * MM
WHEELBASE = 2650 * MM
WHEEL_R = 339 * MM
HL = LENGTH / 2

# The design lives in this table and nowhere else: key stations from tail to nose, as
# (x, half-width, floor z, beltline z, roof z). The loft samples between them, so a station
# is added here to change the shape, not to make the mesh denser.
#
# Two of those need saying. The *beltline* is what a single swept outline gets wrong: a
# car's profile is two curves, the body's shoulder and the glasshouse above it, and lofted
# as one the result is a doorstop -- which is exactly what the first attempt rendered as.
# The half-width is a coke-bottle plan: widest at the rear haunch, waisted at the doors,
# narrower over the front axle. Held constant it reads as a bus from above.
KEY = [
    (-2225, 878, 430, 905, 905),      # tail: cut off square, Kamm rather than tapered away
    (-2150, 896, 395, 917, 919),
    (-2060, 906, 320, 925, 940),
    (-1745, 946, 200, 946, 1000),
    (-1560, 950, 194, 952, 1062),     # backlight, base
    (-1325, 950, 188, 955, 1148),     # rear axle: widest, haunch
    (-900,  942, 180, 948, 1225),
    (-600,  932, 176, 942, 1245),
    (-100,  916, 170, 932, 1250),     # roof apex, at 52% of the length from the nose
    (250,   906, 166, 926, 1232),
    (700,   902, 162, 920, 1090),
    (940,   908, 160, 912, 985),      # cowl: windscreen base
    (1040,  914, 162, 906, 906),      # hood, flat from here forward
    (1325,  928, 172, 866, 866),      # front axle
    (1745,  902, 190, 812, 812),
    (2060,  838, 250, 756, 756),
    (2150,  800, 285, 732, 732),
    (2225,  742, 320, 712, 712),      # nose: a fascia to carry lights and a grille, not a point
]

# Half of the cross-section, as fractions of the station's half-width and of the height of
# the band it belongs to. Mirrored to close the loop.
# The kink at 0.66 is the shoulder crease -- the main body line down the flank. Without it
# the side is one unbroken sheet and reads as a slab whatever the outline does.
FLANK = [(0.965, 0.24), (1.00, 0.52), (0.985, 0.66), (0.945, 0.86), (0.965, 1.00)]
GREENHOUSE = [(0.905, 0.40), (0.815, 0.82), (0.615, 1.00)]  # beltline -> roof edge

# The wheel arch is a rule, not a column of hand-typed numbers: a circular arc over each
# axle, falling to the rocker at its edges. Hand-picked crown heights are how the first
# version put the arch at 495 mm under a 678 mm tyre and sliced the top off every wheel.
ARCH_CROWN, ROCKER_Z, ARCH_HALF = 748, 196, 425
AXLE_X = (-1325, 1325)


def arch_z(x):
    """Height of the outer bottom edge at x: inside an arch it follows the arc, elsewhere it
    sits just under the rocker. Separate from the floor at the centreline, so the arches cost
    no boolean and the underbody stays flat."""
    for axle in AXLE_X:
        dx = abs(x - axle)
        if dx < ARCH_HALF:
            return ROCKER_Z + (ARCH_CROWN - ROCKER_Z) * math.sqrt(1 - (dx / ARCH_HALF) ** 2)
    return ROCKER_Z


def stations():
    """Key stations, resampled so each arch carries enough of them to read as a curve.
    Nine per arch: at four samples the arch came out as a trapezoidal notch."""
    xs = sorted({x for x, *_ in KEY}
                | {axle + d for axle in AXLE_X
                   for d in (-405, -330, -235, -120, 0, 120, 235, 330, 405)})
    out = []
    for x in xs:
        lo = max((k for k in KEY if k[0] <= x), key=lambda k: k[0], default=KEY[0])
        hi = min((k for k in KEY if k[0] >= x), key=lambda k: k[0], default=KEY[-1])
        f = 0.0 if hi[0] == lo[0] else (x - lo[0]) / (hi[0] - lo[0])
        hw, floor, belt, roof = (a + (b - a) * f for a, b in zip(lo[1:], hi[1:]))
        out.append((x, hw, floor, arch_z(x), belt, roof))
    return out


# Wheels: 245/40 R19 -- rim 482.6 mm plus two 98 mm sidewalls, so a 678 mm tyre.
WHEEL_R, RIM_R, DISC_R = 339 * MM, 245 * MM, 168 * MM
TYRE_W, RIM_W, DISC_W = 262 * MM, 210 * MM, 32 * MM
AXLES = (("front", 1325 * MM), ("rear", -1325 * MM))
# Track set so the tyre's outer wall lands just inside the arch lip rather than 50 mm
# under it: tucked-in wheels are the single clearest tell of a body that was drawn
# without them, and the front view showed it immediately.
WHEEL_Y = 790 * MM


# One material per functional group, named for what it is rather than for a look. The colours
# matter for one reason: a workbench render of a single grey subject cannot show whether the
# glasshouse cut landed where it was meant to, and that is what these previews are judged on.
MATERIALS = {
    "body_paint": (0.28, 0.30, 0.34, 1),
    "glass": (0.07, 0.09, 0.12, 1),
    "headlight": (0.86, 0.87, 0.82, 1),
    "taillight": (0.72, 0.06, 0.05, 1),
    "wheel": (0.68, 0.69, 0.72, 1),
    "tyre": (0.055, 0.055, 0.06, 1),
    "brake": (0.33, 0.33, 0.36, 1),
    "trim": (0.10, 0.10, 0.11, 1),
}


def material(name):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = MATERIALS[name]
        mat.use_nodes = False
    return mat


def paint():
    """Assign by name prefix: the object name already says which group it belongs to, so a
    second table mapping objects to materials would only be a place for the two to disagree."""
    for ob in (o for o in bpy.data.objects if o.type == 'MESH'):
        group = next((k for k in MATERIALS if ob.name.startswith(k)), "trim")
        ob.data.materials.clear()
        ob.data.materials.append(material(group))
        ob.color = MATERIALS[group]


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def new_object(name, mesh):
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(ob)
    return ob


def ring(x, half_width, z_floor, z_arch, z_belt, z_roof):
    """A closed cross-section: floor, up the right flank, in across the roof, down the left.

    Closed, unlike make_demo_vehicle's open-bottomed ring: that one exists to give solidify
    work to do, this one has to be watertight without help.

    Where z_roof == z_belt the greenhouse points do not collapse -- they stay at beltline
    height and step inward in Y, which is a flat deck. That is why the hood and the rear
    deck need no special case."""
    x, hw = x * MM, half_width * MM
    z0, arch, belt, roof = z_floor * MM, z_arch * MM, z_belt * MM, z_roof * MM
    right = [(x, hw * 0.66, z0), (x, hw * 0.93, arch)]
    right += [(x, hw * fy, arch + (belt - arch) * fz) for fy, fz in FLANK]
    right += [(x, hw * fy, belt + (roof - belt) * fz) for fy, fz in GREENHOUSE]
    return ([(x, 0.0, z0)] + right + [(x, 0.0, roof)]
            + [(x, -y, z) for _, y, z in reversed(right)])


# Which bands of the section are glass, and over which stations. A window cannot be a
# separate panel tucked inside a closed body -- the body surface would simply hide it. The
# glasshouse is cut out of the loft instead: both objects are built from the same rings and
# share their edges exactly, so there is no gap to see through and nothing intersects.
# Indices are into the ring: 7-9 climb the right side of the greenhouse, 12-14 the left.
# Stopping at 8 left the glass lying on the shoulder like a stripe; it has to run all the way
# to the roof edge, so what stays painted up there is the roof panel and nothing else.
DLO_BANDS = {7, 8, 9, 12, 13, 14}
DLO_X = (-1560, 940)          # backlight base to windscreen base


def loft(rings, name, cutout=None, cutout_name="glass"):
    """Bridge consecutive rings into quads and cap both ends.

    Faces the cutout claims go to a second object; the rest stays on the first. Together
    they are the closed tube the single-object version produced."""
    bm, cut = bmesh.new(), bmesh.new()
    loops = [[bm.verts.new(p) for p in r] for r in rings]
    cut_loops = [[cut.verts.new(p) for p in r] for r in rings]
    bm.verts.ensure_lookup_table(); cut.verts.ensure_lookup_table()
    for k, (a, b) in enumerate(zip(loops, loops[1:])):
        ca, cb = cut_loops[k], cut_loops[k + 1]
        x0, x1 = rings[k][0][0], rings[k + 1][0][0]
        inside = cutout and DLO_X[0] * MM <= x0 and x1 <= DLO_X[1] * MM
        for i in range(len(a)):
            j = (i + 1) % len(a)
            target, quad = ((cut, (ca[i], ca[j], cb[j], cb[i])) if inside and i in cutout
                            else (bm, (a[i], a[j], b[j], b[i])))
            target.faces.new(quad)
    bm.faces.new(list(reversed(loops[0])))
    bm.faces.new(loops[-1])
    made = []
    for mesh_bm, mesh_name in ((bm, name), (cut, cutout_name)):
        if not mesh_bm.faces:
            mesh_bm.free(); continue
        bmesh.ops.delete(mesh_bm, geom=[v for v in mesh_bm.verts if not v.link_faces], context='VERTS')
        bmesh.ops.recalc_face_normals(mesh_bm, faces=mesh_bm.faces[:])
        mesh = bpy.data.meshes.new(mesh_name)
        mesh_bm.to_mesh(mesh); mesh_bm.free()
        made.append(new_object(mesh_name, mesh))
    return made


def box(name, x, y, z):
    """A closed cuboid from three (min, max) pairs in millimetres. Every bolt-on below is one
    of these: at this level of detail a lamp is a lens-shaped block, and modelling it as
    anything more would be the manufacturing detail the brief rules out."""
    (x0, x1), (y0, y1), (z0, z1) = ((a * MM, b * MM) for a, b in (x, y, z))
    verts = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
             (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return new_object(name, mesh)


def tube(name, r_out, r_in, width, centre, segments=28):
    """An annulus swept along Y: the tyre is a real ring, so the rim sits inside it touching
    rather than buried in it. A solid cylinder for the tyre would have put the whole rim
    inside solid geometry, which is the "no intersecting geometry" the brief rules out."""
    bm = bmesh.new()
    cx, cy, cz = centre
    loops = []
    for y in (cy - width / 2, cy + width / 2):
        for r in (r_out, r_in):
            loops.append([bm.verts.new((cx + r * math.cos(a), y, cz + r * math.sin(a)))
                          for a in (2 * math.pi * i / segments for i in range(segments))])
    bm.verts.ensure_lookup_table()
    outer_a, inner_a, outer_b, inner_b = loops
    for a, b in ((outer_a, outer_b), (inner_b, inner_a), (inner_a, outer_a), (outer_b, inner_b)):
        for i in range(segments):
            j = (i + 1) % segments
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh); bm.free()
    return new_object(name, mesh)


def disc(name, radius, width, centre, segments=28):
    """A closed cylinder on the Y axis, for the rim barrel and the brake disc."""
    return tube(name, radius, radius * 0.001, width, centre, segments)


clear()
body, glass = loft([ring(*s) for s in stations()], "body_paint", DLO_BANDS, "glass")

# Bolt-ons. Each straddles the surface it sits in rather than floating on it or being buried:
# the nose cap is a flat face at x = 2225, so a lamp spanning 2200 to 2232 reads as recessed
# into the fascia with a few millimetres proud, which is what a lamp does.
for side, sign in (("left", -1), ("right", 1)):
    box(f"headlight_{side}", (2196, 2232), (sign * 250, sign * 640), (596, 690))
    box(f"taillight_{side}", (-2232, -2198), (sign * 210, sign * 690), (712, 806))
    # Mirror on a short stalk off the door skin: the housing clears the flank, the stalk
    # bridges the gap, so nothing floats and nothing is buried.
    box(f"trim_mirror_{side}", (628, 760), (sign * 946, sign * 1046), (928, 1004))
    box(f"trim_mirror_stalk_{side}", (664, 724), (sign * 892, sign * 950), (916, 962))
    # Air intake ahead of the rear arch, the one styling cue that says where the engine is.
    box(f"trim_intake_{side}", (-1010, -880), (sign * 902, sign * 952), (404, 536))

box("trim_grille", (2192, 2228), (-470, 470), (372, 548))
box("trim_splitter", (2110, 2246), (-700, 700), (300, 344))
box("trim_diffuser", (-2246, -2090), (-660, 660), (378, 452))

# Wheels: built on both sides explicitly rather than mirrored. A mirror modifier left
# unapplied is the trap make_demo_vehicle exists to demonstrate; this subject is meant to
# leave the generator ready to use.
for end, x in AXLES:
    for side, y in (("left", -WHEEL_Y), ("right", WHEEL_Y)):
        tube(f"tyre_{end}_{side}", WHEEL_R, RIM_R, TYRE_W, (x, y, WHEEL_R))
        disc(f"wheel_{end}_{side}", RIM_R, RIM_W, (x, y, WHEEL_R))
        disc(f"brake_{end}_{side}", DISC_R, DISC_W, (x, y * 0.88, WHEEL_R))


def report():
    """Two counts, because they mean different things. Per object, the body and the glass are
    each open along the window aperture they share -- that is the cut, not a defect. Welded
    together the whole subject must still be closed, and that is the number to watch."""
    objs = [o for o in bpy.data.objects if o.type == 'MESH']
    per_object = 0
    for o in objs:
        bm = bmesh.new(); bm.from_mesh(o.data)
        per_object += sum(1 for e in bm.edges if len(e.link_faces) != 2)
        bm.free()
    bm = bmesh.new()
    for o in objs:
        bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-6)
    welded = sum(1 for e in bm.edges if len(e.link_faces) != 2)
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = [min(p[i] for p in pts) / MM for i in range(3)]
    hi = [max(p[i] for p in pts) / MM for i in range(3)]
    bm.free()
    print("sportscar: %d objects  %d verts  open edges %d per-object / %d welded  "
          "bbox mm X %.0f Y %.0f Z %.0f  z_min %.0f"
          % (len(objs), sum(len(o.data.vertices) for o in objs), per_object, welded,
             hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], lo[2]))


def preview(path):
    """Four workbench views beside the .blend: the silhouette is judged by eye, not by a
    vertex count, and run_012 is explicit that nothing else confirms it reads as a car."""
    scene = bpy.context.scene
    objs = [o for o in bpy.data.objects if o.type == 'MESH']
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector([min(p[i] for p in pts) for i in range(3)])
    hi = Vector([max(p[i] for p in pts) for i in range(3)])
    centre, radius = (lo + hi) / 2, (hi - lo).length / 2
    data = bpy.data.cameras.new("preview"); data.type = 'ORTHO'; data.ortho_scale = radius * 2.2
    cam = bpy.data.objects.new("preview", data)
    scene.collection.objects.link(cam); scene.camera = cam
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", 'SUN'))
    scene.collection.objects.link(sun); sun.rotation_euler = (0.9, 0.2, 0.6)
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.color_type = 'MATERIAL'
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.show_shadows = True
    scene.render.resolution_x, scene.render.resolution_y = 1200, 800
    for view, direction in (("3q", Vector((-1.1, -1.0, 0.5))), ("side", Vector((0, -1, 0))),
                            ("front", Vector((1, 0, 0))), ("rear", Vector((-1, 0, 0))),
                            ("top", Vector((0, 0, 1)))):
        direction = direction.normalized()
        cam.location = centre + direction * radius * 4
        # Straight down leaves track-to's up vector free to pick anything, and the plan came
        # out rotated 45 degrees. Nose up the frame is the only reading worth having.
        cam.rotation_euler = ((0, 0, math.pi / 2) if view == "top"
                              else (-direction).to_track_quat('-Z', 'Y').to_euler())
        scene.render.filepath = os.path.splitext(path)[0] + f"_{view}.png"
        bpy.ops.render.render(write_still=True)


paint()
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
path = next((a for a in args if not a.startswith("--")), None) or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "out", "sportscar.blend")
os.makedirs(os.path.dirname(path), exist_ok=True)
report()
bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
if "--preview" in args:
    preview(path)

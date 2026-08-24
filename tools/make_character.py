"""Build a T-pose character one stage at a time, as operations rather than as a script.

Same shape as tools/make_vise.py: each stage is a transform whose input is the previous
stage's output, so the six states form one chain the viewer walks. Voir run_012, steps 14-15.

Everything is swept from elliptical sections whose radii change at every station. That is the
one decision that keeps this off the mannequin: a limb built as a cylinder has one radius and
a circular section, and no amount of detail afterwards recovers from either.

Unlike the hammer and the vise, this one is shaded smooth and lightly subdivided at the last
stage. The faceted house style belongs to the application's own icon language; a character is
not an icon, and the brief asks for deformation-friendly surfaces.

    meshanvil run make_character <file.blend> --set stage=N
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

STAGE_NAMES = {1: "Proportions", 2: "Primary volumes", 3: "Anatomy",
               4: "Head and face", 5: "Hands and feet", 6: "Final"}

# --- proportions ------------------------------------------------------------------------
# A 1800 mm figure at 7.5 heads. Every landmark below is a height in millimetres, and every
# volume in every stage is placed off these and nothing else -- which is what makes stage 1
# a real proportion check rather than a decoration: if the guide is wrong, so is the model.
HEIGHT = 1800
HEAD_H = HEIGHT / 7.5          # 240
CROWN, CHIN = 1800, 1560
SHOULDER_Z, NIPPLE_Z, WAIST_Z = 1462, 1320, 1140
HIP_Z, CROTCH_Z, KNEE_Z, ANKLE_Z = 940, 880, 500, 78
# The subject faces +X, as every other subject in this project does, so lateral is Y and depth
# is X. Built facing +Y first, which put the body 90 degrees from its own feet and made the
# engine's "front" render show a profile -- the label is what caught it.
SHOULDER_Y, ELBOW_Y, WRIST_Y, HAND_TIP_Y = 205, 478, 742, 928
LEG_Y = 98

MATERIALS = {
    "skin": (0.72, 0.56, 0.47, 1),
    "guide": (0.93, 0.62, 0.36, 1),     # #ed9e5c, the accent: scaffolding, not the model
    "eye": (0.10, 0.11, 0.13, 1),
    "hair": (0.17, 0.15, 0.15, 1),
}

SEGMENTS = 16


def new_object(name, mesh):
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(ob)
    return ob


def sweep(name, axis, stations, segments=SEGMENTS, close=True):
    """Loft elliptical rings along one axis.

    A station is (t, a, b, ra, rb): the position along the axis, the section's centre in the
    other two, and its two radii. Two radii, never one -- a human limb is oval everywhere and
    a circular section is the tell that gives a mannequin away at any polygon count."""
    rings = []
    for t, a, b, ra, rb in stations:
        ring = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            u, v = ra * math.cos(angle), rb * math.sin(angle)
            point = {"x": (t, a + u, b + v),
                     "y": (a + u, t, b + v),
                     "z": (a + u, b + v, t)}[axis]
            ring.append(tuple(c * MM for c in point))
        rings.append(ring)

    bm = bmesh.new()
    loops = [[bm.verts.new(p) for p in r] for r in rings]
    bm.verts.ensure_lookup_table()
    for lo, hi in zip(loops, loops[1:]):
        for i in range(segments):
            j = (i + 1) % segments
            bm.faces.new((lo[i], lo[j], hi[j], hi[i]))
    if close:
        bm.faces.new(list(reversed(loops[0])))
        bm.faces.new(loops[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return new_object(name, mesh)


def marker(name, centre, size):
    """A guide cube. Stage 1 is a skeleton of these, and a later stage deletes them: a guide
    that survives into the model is a floating fragment, which is the thing to avoid."""
    x, y, z = centre
    h = size / 2
    mesh = bpy.data.meshes.new(name)
    verts = [((x + dx * h) * MM, (y + dy * h) * MM, (z + dz * h) * MM)
             for dx in (-1, 1) for dy in (-1, 1) for dz in (-1, 1)]
    mesh.from_pydata(verts, [], [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
                                 (1, 5, 7, 3), (3, 7, 6, 2), (2, 6, 4, 0)])
    mesh.update()
    return new_object(name, mesh)


def find(name):
    return bpy.data.objects.get(name)


def each(prefix):
    return [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(prefix)]


def swell(ob, axis, at, spread, amount):
    """Push a band of the surface out from its own axis, smoothly.

    This is what stage 3 does instead of rebuilding: a deltoid, a calf belly and a waist are
    all the same operation with a different sign, applied to the geometry stage 2 left. A
    stage that replaced those meshes would not be a refinement, it would be a second model."""
    index = "xyz".index(axis)
    others = [i for i in range(3) if i != index]
    centre = [sum(v.co[i] for v in ob.data.vertices) / len(ob.data.vertices) for i in range(3)]
    for v in ob.data.vertices:
        distance = (v.co[index] / MM - at) / spread
        factor = 1 + amount * math.exp(-distance * distance)
        for i in others:
            v.co[i] = centre[i] + (v.co[i] - centre[i]) * factor


def material(name):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = MATERIALS[name]
        mat.use_nodes = False
    return mat


def paint():
    for ob in (o for o in bpy.data.objects if o.type == 'MESH'):
        group = ("guide" if ob.name.startswith("guide") else
                 "eye" if ob.name.startswith("eye") else
                 "hair" if ob.name.startswith("hair") else "skin")
        ob.data.materials.clear()
        ob.data.materials.append(material(group))
        ob.color = MATERIALS[group]


# --- stages -------------------------------------------------------------------------------

def stage_1_proportions():
    """A skeleton of landmarks. Nothing here survives into the model; it exists to be looked
    at against the heights above before a single volume is built on them."""
    for name, centre in (
            ("guide_head", (0, 0, (CROWN + CHIN) / 2)),
            ("guide_neck", (0, 0, (CHIN + SHOULDER_Z) / 2)),
            ("guide_chest", (0, 0, NIPPLE_Z)),
            ("guide_waist", (0, 0, WAIST_Z)),
            ("guide_pelvis", (0, 0, HIP_Z)),
    ):
        marker(name, centre, 70)
    for side in (-1, 1):
        for name, centre in (
                (f"guide_shoulder_{side}", (0, side * SHOULDER_Y, SHOULDER_Z)),
                (f"guide_elbow_{side}", (0, side * ELBOW_Y, SHOULDER_Z)),
                (f"guide_wrist_{side}", (0, side * WRIST_Y, SHOULDER_Z)),
                (f"guide_hip_{side}", (0, side * LEG_Y, HIP_Z)),
                (f"guide_knee_{side}", (0, side * LEG_Y, KNEE_Z)),
                (f"guide_ankle_{side}", (0, side * LEG_Y, ANKLE_Z)),
        ):
            marker(name, centre, 56)
    # The spine, as a thin swept rod: the one guide that is a line rather than a point.
    sweep("guide_spine", "z", [(z, -20, 0, 12, 12)
                               for z in (HIP_Z, WAIST_Z, NIPPLE_Z, SHOULDER_Z, CHIN)])


def stage_2_volumes():
    """The anatomical masses, each swept from its own varying section."""
    sweep("torso", "z", [
        (CROTCH_Z - 20, 0, 0, 108, 150),
        (HIP_Z, 0, 0, 116, 178),
        (1020, -4, 0, 104, 158),
        (WAIST_Z, -6, 0, 100, 146),
        (1240, 0, 0, 108, 168),
        (NIPPLE_Z, 4, 0, 116, 192),
        (1400, 0, 0, 114, 208),
        (SHOULDER_Z, -6, 0, 102, 215),
    ])
    sweep("neck", "z", [(SHOULDER_Z - 10, -10, 0, 62, 66), (1510, -6, 0, 58, 60),
                        (CHIN + 6, 0, 0, 62, 64)])
    sweep("head", "z", [
        (CHIN - 4, 6, 0, 62, 52), (1592, 4, 0, 82, 70), (1636, 0, 0, 94, 80),
        (1690, -4, 0, 98, 84), (1740, -6, 0, 92, 80), (1782, -8, 0, 68, 60),
        (CROWN, -8, 0, 30, 26),
    ])
    for side in (-1, 1):
        tag = "l" if side < 0 else "r"
        # Every joint overlaps its neighbour by tens of millimetres, not by four. Catmull-Clark
        # pulls a capped tube end inward, so parts that merely touched came apart at every
        # elbow, knee, wrist and ankle once stage 6 subdivided them -- disconnected fragments,
        # which is the one thing a base mesh must not have.
        sweep(f"upperarm_{tag}", "y", [
            (side * (SHOULDER_Y - 70), 0, SHOULDER_Z - 6, 62, 58),
            (side * 300, 0, SHOULDER_Z - 8, 54, 50),
            (side * (ELBOW_Y + 26), 0, SHOULDER_Z - 10, 45, 42),
        ])
        sweep(f"forearm_{tag}", "y", [
            (side * (ELBOW_Y - 34), 0, SHOULDER_Z - 10, 47, 44),
            (side * 600, 0, SHOULDER_Z - 10, 40, 38),
            (side * (WRIST_Y + 26), 0, SHOULDER_Z - 10, 32, 27),
        ])
        # Palms down: the hand is wide front to back and thin vertically, which is the pose
        # rather than a shape choice.
        sweep(f"hand_{tag}", "y", [
            (side * (WRIST_Y - 26), 0, SHOULDER_Z - 10, 31, 26),
            (side * 790, 0, SHOULDER_Z - 10, 44, 22),
            (side * 860, 0, SHOULDER_Z - 10, 46, 20),
            (side * HAND_TIP_Y, 0, SHOULDER_Z - 10, 32, 16),
        ])
        sweep(f"thigh_{tag}", "z", [
            (HIP_Z + 46, 0, side * (LEG_Y - 6), 98, 94),
            (760, 0, side * LEG_Y, 88, 84),
            (KNEE_Z - 26, -4, side * LEG_Y, 66, 62),
        ])
        sweep(f"calf_{tag}", "z", [
            (KNEE_Z + 34, -4, side * LEG_Y, 66, 62),
            (380, 6, side * LEG_Y, 58, 56),
            (200, 2, side * LEG_Y, 42, 40),
            (ANKLE_Z - 34, 0, side * LEG_Y, 35, 32),
        ])
        sweep(f"foot_{tag}", "x", [
            (-92, side * LEG_Y, 58, 44, 52),
            (0, side * LEG_Y, 40, 50, 40),
            (110, side * (LEG_Y + 4), 30, 52, 30),
            (168, side * (LEG_Y + 6), 22, 44, 22),
        ])


def stage_3_anatomy():
    """The guide comes out and the tubes stop being tubes."""
    for ob in each("guide"):
        bpy.data.objects.remove(ob, do_unlink=True)
    for side in (-1, 1):
        tag = "l" if side < 0 else "r"
        swell(find(f"upperarm_{tag}"), "y", side * 250, 90, 0.16)     # deltoid and biceps
        swell(find(f"upperarm_{tag}"), "y", side * ELBOW_Y, 46, -0.10)  # elbow tucks in
        swell(find(f"forearm_{tag}"), "y", side * 560, 90, 0.14)      # forearm belly
        swell(find(f"forearm_{tag}"), "y", side * WRIST_Y, 40, -0.12)  # wrist
        swell(find(f"calf_{tag}"), "z", 400, 90, 0.15)                # calf belly
        swell(find(f"calf_{tag}"), "z", ANKLE_Z, 60, -0.10)           # ankle
        swell(find(f"thigh_{tag}"), "z", 860, 110, 0.10)              # upper thigh mass
        swell(find(f"thigh_{tag}"), "z", KNEE_Z, 70, -0.06)           # knee
    swell(find("torso"), "z", WAIST_Z, 90, -0.07)                     # waist
    swell(find("torso"), "z", 1380, 110, 0.06)                        # chest
    swell(find("neck"), "z", SHOULDER_Z, 34, 0.12)                    # neck into shoulders
    # Deltoid caps: the one place a swept limb cannot reach, because the mass belongs to
    # neither the arm nor the torso.
    for side in (-1, 1):
        tag = "l" if side < 0 else "r"
        sweep(f"deltoid_{tag}", "y", [
            (side * (SHOULDER_Y - 78), 0, SHOULDER_Z - 8, 60, 54),
            (side * (SHOULDER_Y + 4), 0, SHOULDER_Z - 4, 68, 64),
            (side * (SHOULDER_Y + 74), 0, SHOULDER_Z - 10, 56, 52),
        ])


def stage_4_head():
    """Skull, jaw, nose, brow, ears, eyes. Shaped onto the head, not floated in front of it."""
    head = find("head")
    for v in head.data.vertices:
        z = v.co.z / MM
        # Flatten the back of the skull and pull the jaw forward: a swept stack of ellipses
        # is an egg until something says which end is the face. Depth is X.
        if z < 1636 and v.co.x > 0:
            v.co.x += (0.16 * (1636 - z)) * MM
        if z > 1700 and v.co.x < 0:
            v.co.x *= 0.92
    # Every feature has to reach the skull's own surface, which is at x ~ 88 to 94 across the
    # face. Placed by eye they all sat 25 mm inside it: geometrically present, invisible from
    # any angle, and impossible to spot in a render of a whole 1800 mm figure. Measuring the
    # head's front before placing anything on it is the only way this gets caught.
    sweep("jaw", "z", [(CHIN - 2, 44, 0, 38, 44), (1590, 30, 0, 60, 64), (1630, 14, 0, 76, 74)])
    sweep("nose", "x", [(66, 0, 1672, 16, 15), (108, 0, 1662, 21, 19), (132, 0, 1646, 15, 13)])
    sweep("brow", "z", [(1692, 84, 0, 20, 74), (1712, 80, 0, 17, 70)])
    for side in (-1, 1):
        tag = "l" if side < 0 else "r"
        sweep(f"eye_{tag}", "x", [(72, side * 36, 1680, 16, 16), (96, side * 36, 1680, 13, 13)],
              segments=12)
        sweep(f"ear_{tag}", "y", [(side * 76, -8, 1674, 32, 13), (side * 96, -6, 1674, 27, 10)],
              segments=12)
    sweep("mouth", "x", [(74, 0, 1600, 28, 7), (96, 0, 1600, 23, 6)], segments=12)
    sweep("hair", "z", [(1660, -10, 0, 100, 88), (1712, -12, 0, 102, 90),
                        (1768, -12, 0, 84, 74), (1798, -10, 0, 34, 30)])


def stage_5_hands_feet():
    """Four fingers and a thumb, and a foot that has a heel, an arch and toes."""
    for side in (-1, 1):
        tag = "l" if side < 0 else "r"
        palm = find(f"hand_{tag}")
        # The palm stops where the fingers start: without this the fingers grow out of a
        # mitten and the hand reads as one paddle.
        for v in palm.data.vertices:
            if abs(v.co.y) / MM > 866:
                v.co.y = side * 866 * MM
        # Fingers spread front to back across the palm, because the palm faces down.
        for index, (offset, length, radius) in enumerate(
                ((-33, 128, 13), (-11, 140, 13.5), (11, 132, 13), (32, 112, 11.5))):
            sweep(f"finger_{tag}{index}", "y", [
                (side * 832, offset, SHOULDER_Z - 10, radius, radius * 0.86),
                (side * (858 + length * 0.55), offset * 1.06, SHOULDER_Z - 11, radius * 0.9,
                 radius * 0.78),
                (side * (858 + length), offset * 1.1, SHOULDER_Z - 12, radius * 0.62,
                 radius * 0.54),
            ], segments=10)
        # The thumb points forward, not down: that is what "palms facing downward" means.
        sweep(f"thumb_{tag}", "x", [
            (46, side * 800, SHOULDER_Z - 12, 15, 14),
            (96, side * 828, SHOULDER_Z - 13, 13, 12),
            (136, side * 846, SHOULDER_Z - 14, 10, 9),
        ], segments=10)
        foot = find(f"foot_{tag}")
        for v in foot.data.vertices:
            x = v.co.x / MM
            # Lift the arch: the instep is the difference between a foot and a shoe box.
            if -20 < abs(x) < 90 and v.co.z / MM < 34:
                v.co.z += 12 * MM
        sweep(f"toes_{tag}", "x", [
            (140, side * (LEG_Y + 6), 22, 46, 22),
            (204, side * (LEG_Y + 6), 18, 42, 18),
            (232, side * (LEG_Y + 4), 15, 32, 15),
        ], segments=12)


def stage_6_final():
    """One level of Catmull-Clark and smooth normals, applied, not left as a modifier.

    Level one, not three: the brief asks for reasonable density and deformation-friendly
    surfaces, and a subdivided base mesh is both. Level three would be a sculpt nobody can
    edit, which is the same mistake as remeshing."""
    for ob in (o for o in bpy.data.objects if o.type == 'MESH'):
        modifier = ob.modifiers.new("subsurf", 'SUBSURF')
        modifier.levels = modifier.render_levels = 1
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        for polygon in ob.data.polygons:
            polygon.use_smooth = True
    paint()


STAGES = {1: stage_1_proportions, 2: stage_2_volumes, 3: stage_3_anatomy,
          4: stage_4_head, 5: stage_5_hands_feet, 6: stage_6_final}

if STAGE not in STAGES:
    message = f"no stage {STAGE}: this character has {len(STAGES)}"
    if REPORT:
        REPORT.failed(message)
        REPORT.write()
    sys.exit(message)

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.before(reporting.measure_scene())

STAGES[STAGE]()
if STAGE < 6:
    paint()

source = Path(bpy.data.filepath)
OUT = source.with_name(f"{re.sub(r'(_s[0-9]+)+$', '', source.stem)}_s{STAGE}.blend")

if RENDER:
    views.shoot(REPORT, JOB, ROOT, OUT.stem)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
pts = [o.matrix_world @ v.co for o in meshes for v in o.data.vertices]
low = min(p.z for p in pts) / MM if pts else 0
high = max(p.z for p in pts) / MM if pts else 0
print("[make_character] stage %d %s: %d objects, height %.0f mm, feet at %.0f"
      % (STAGE, STAGE_NAMES[STAGE], len(meshes), high - low, low))

if REPORT:
    REPORT.after(reporting.measure_scene())
    REPORT.report["params"]["stage_name"] = "%02d %s" % (STAGE, STAGE_NAMES[STAGE])
    REPORT.finding("stage", number=STAGE, name=STAGE_NAMES[STAGE], objects=len(meshes),
                   height_mm=round(high - low), feet_z_mm=round(low))
    if STAGE > 1 and abs(low) > 2:
        REPORT.warn("feet_not_on_the_ground")
    REPORT.cites("run_012_build_a_recognizable_low_poly_subject_from_primitives")
    REPORT.output(str(OUT))
    REPORT.write()

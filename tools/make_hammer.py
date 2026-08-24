"""Generate the meshanvil hammer: the mascot object, in the application's own visual language.

The style is not invented here, it is read off viewer/icon.png -- a faceted low-poly anvil in
graphite with its working surfaces in the accent copper (#ed9e5c, the viewer's --active). So
this is flat-shaded and faceted on purpose, with chamfers wide enough to read as facets rather
than as softening. A smooth, subdivided, photoreal hammer would be a better hammer and a worse
meshanvil asset.

Semantic parts, one object per material: the head, its two struck faces, the handle, and the
wedge that locks the handle in the eye. Nothing is remeshed; what leaves this file is the
editable master. Voir run_012, step 9.

    blender -b -P tools/make_hammer.py -- <destination.blend>
"""
import bpy, bmesh, os, sys, math
from mathutils import Vector

MM = 0.001

# Palette lifted from viewer/viewer.css: --active for the copper, the panel greys for the rest.
MATERIALS = {
    "head": (0.20, 0.21, 0.23, 1),
    "face": (0.93, 0.62, 0.36, 1),      # #ed9e5c, the accent the icon puts on working surfaces
    "handle": (0.13, 0.13, 0.15, 1),
    "wedge": (0.78, 0.50, 0.29, 1),
}

# The head, along its striking axis. (x, half-width, half-height): waisted between the eye and
# each face, then flaring back out at the faces themselves. That flare is the whole silhouette
# -- a head that tapers monotonically to its ends reads as a wedge of cheese, and a head of
# constant section reads as a block. Struck faces on a forged hammer are wider than the neck
# behind them, and saying so in three stations is what makes this look designed.
HEAD = [
    (-100, 36.0, 36.0),   # rear face
    (-91, 39.0, 39.0),    # face flare
    (-68, 28.5, 30.0),    # waist: deeper than it was, the silhouette lives on this
    (-34, 33.5, 40.0),
    (0, 39.5, 47.0),      # eye boss: tallest, where the handle passes through
    (34, 33.5, 40.0),
    (68, 28.5, 30.0),     # waist
    (91, 39.5, 39.5),     # face flare
    (100, 36.5, 36.5),    # front face, the broad one
]

# The handle, bottom to top. (z, half-depth along the striking axis, half-width across it):
# an oval, never a circle, and it swells at the very bottom so the hand has something to stop
# against. Its top sits inside the eye.
# Shortened and thickened after the first render: at 432 mm against a 200 mm head the shaft
# read as a stick, and this is a mascot before it is a tool. The butt swell is exaggerated for
# the same reason -- at true proportions it disappears at icon size.
HANDLE = [
    (0, 30.0, 24.0),      # butt swell
    (18, 32.0, 25.5),
    (46, 25.5, 20.0),
    (120, 23.5, 18.5),
    (215, 22.5, 17.5),
    (285, 22.0, 17.0),
    (325, 23.5, 18.0),    # thickens again into the eye: a shaft that thins to nothing there
    (356, 25.0, 19.0),    # would read as a stick pushed into a block
]
HEAD_Z = 306                # head centre, near the top of the handle
HANDLE_CURVE = 13           # how far the butt swings back from the head's axis, in mm


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(name):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = MATERIALS[name]
        mat.use_nodes = False
    return mat


def octagon(half_a, half_b, chamfer=0.30):
    """A rectangle with its corners cut: eight points, not four and not thirty-two.

    This is the section for everything here. A circle would give a turned bar, a rectangle a
    sawn billet; the cut corner is what a forged bar under a hammer actually becomes, and it
    is also the facet the icon is drawn in."""
    a, b, c = half_a, half_b, chamfer
    return [(a, b * (1 - c)), (a * (1 - c), b), (-a * (1 - c), b), (-a, b * (1 - c)),
            (-a, -b * (1 - c)), (-a * (1 - c), -b), (a * (1 - c), -b), (a, -b * (1 - c))]


def forged(x, span):
    """A hair of asymmetry, in millimetres, so the two sides of the head are not machine-equal.

    Deterministic on purpose: a random seed would make two runs of this generator produce
    meshes that differ by a hundredth of a millimetre, which is exactly the noise that makes a
    report chain's before/after numbers stop meaning anything."""
    return 0.55 * math.sin(x / span * 5.1) + 0.30 * math.sin(x / span * 11.3)


def loft(rings, name, slots, segment_slot=None):
    """Bridge rings into quads, cap both ends, and give named segments their own material slot.

    The struck faces were separate objects first, sharing a seam with the head the way the
    sports car's glass shares one with its body. That works when nothing moves afterwards, and
    a bevel moves things: chamfering each part on its own displaced the shared seam twice,
    independently, and 64 edges survived the weld. A material slot is the right tool for two
    finishes on one forging -- the mesh stays closed and the bevel has nothing to tear."""
    bm = bmesh.new()
    loops = [[bm.verts.new(p) for p in r] for r in rings]
    bm.verts.ensure_lookup_table()
    index = {slot: i for i, slot in enumerate(slots)}
    tagged = []
    for k in range(len(rings) - 1):
        a, b = loops[k], loops[k + 1]
        slot = index[(segment_slot or {}).get(k, slots[0])]
        for i in range(len(a)):
            j = (i + 1) % len(a)
            tagged.append((bm.faces.new((a[i], a[j], b[j], b[i])), slot))
    tagged.append((bm.faces.new(list(reversed(loops[0]))),
                   index[(segment_slot or {}).get(0, slots[0])]))
    tagged.append((bm.faces.new(loops[-1]),
                   index[(segment_slot or {}).get(len(rings) - 2, slots[0])]))
    for face, slot in tagged:
        face.material_index = slot
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    # One segment, not four: the chamfer is meant to be seen as a facet, in the icon's
    # language, rather than to disappear into a rounded edge.
    bmesh.ops.bevel(bm, geom=bm.verts[:] + bm.edges[:], offset=1.6 * MM, segments=1,
                    affect='EDGES', clamp_overlap=True)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(ob)
    for slot in slots:
        mesh.materials.append(material(slot))
    ob.color = MATERIALS[slots[0]]
    return ob


clear()

# --- head: swept along X, the striking axis, and lifted to sit on the handle's top.
head_rings = []
for x, ha, hb in HEAD:
    wobble = forged(x, 100)
    head_rings.append([(x * MM, a * MM, (HEAD_Z + b + wobble) * MM)
                       for a, b in octagon(ha, hb + wobble)])
# The first and last segments are the struck faces, and they are the copper.
loft(head_rings, "head", ["head", "face"], {0: "face", len(HEAD) - 2: "face"})

# --- handle: swept along Z, oval section, curving back from the head's axis toward the butt.
handle_rings = []
for z, ha, hb in HANDLE:
    t = 1 - z / HANDLE[-1][0]
    lean = -HANDLE_CURVE * t * t
    handle_rings.append([((lean + a) * MM, b * MM, z * MM)
                         for a, b in octagon(ha, hb)])
loft(handle_rings, "handle", ["handle"])

# --- the wedge driven into the handle's top to lock it in the eye. Small, and the one place a
# hammer shows a second metal, which is where the icon's copper belongs on this object.
# Flat and wide rather than tall: proud of the eye by a few millimetres it reads as the wedge
# capping the handle, and standing up it read as a cork stopper.
wedge_rings = [[(a * MM, b * MM, z * MM) for a, b in octagon(ha, hb, 0.42)]
               for z, ha, hb in ((344, 21.0, 16.0), (356, 25.5, 19.5), (362, 23.5, 18.0))]
loft(wedge_rings, "wedge", ["wedge"])

# --- centre the whole object on the world origin, keeping real millimetres.
objs = [o for o in bpy.data.objects if o.type == 'MESH']
pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
centre = Vector([(min(p[i] for p in pts) + max(p[i] for p in pts)) / 2 for i in range(3)])
for o in objs:
    o.location -= centre
# matrix_world is cached: measuring before this update reports where the object used to be.
bpy.context.view_layer.update()

pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
lo = [min(p[i] for p in pts) / MM for i in range(3)]
hi = [max(p[i] for p in pts) / MM for i in range(3)]
# Two counts, as on the sports car: the head and its faces are each open along the seam they
# share, which is the split and not a defect. Welded, the whole object must still close.
open_edges = 0
for o in objs:
    bm = bmesh.new(); bm.from_mesh(o.data)
    open_edges += sum(1 for e in bm.edges if len(e.link_faces) != 2)
    bm.free()
bm = bmesh.new()
for o in objs:
    bm.from_mesh(o.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-6)
welded = sum(1 for e in bm.edges if len(e.link_faces) != 2)
bm.free()
print("hammer: %d objects  %d verts  open edges %d per-object / %d welded  "
      "bbox mm X %.0f Y %.0f Z %.0f  centred %.1f %.1f %.1f"
      % (len(objs), sum(len(o.data.vertices) for o in objs), open_edges, welded,
         hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2],
         (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))

path = next((a for a in (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
             if not a.startswith("--")), None) or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "out", "hammer.blend")
os.makedirs(os.path.dirname(path), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)

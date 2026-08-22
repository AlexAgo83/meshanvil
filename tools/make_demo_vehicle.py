"""Generate a vehicle-scale demonstration subject from primitives -- no donor file, nothing
to license, everything regenerates. Built to carry the same class of defects a real render
asset carries, on purpose, so the demonstration chain has the same lesson to tell:

- The body is one continuous shell: a rounded cross-section ring, open along the bottom (no
  floor pan, a common render-only export trait), swept along the length through stations that
  narrow and lower at the nose and tail. It has no wall thickness anywhere; solidify has real
  work to do on it.
- The wheels are built on one side and mirrored, unapplied: baking the stack doubles their
  vertex count, and joining without applying would silently drop it.
- One object inside the shell and under a belly panel that covers most, not all, of the open
  underside -- ray_visibility reads it as mostly hidden rather than reliably sealed, and that
  is reported honestly rather than claimed as a guaranteed-invisible part.
- One coincident duplicate, for scan_defects to find.
- Authored 1.6x oversize, so recenter's scale decision is doing real work, not a no-op.

    blender -b -P tools/make_demo_vehicle.py -- <destination.blend>
"""
import bpy, bmesh, os, sys, math
from mathutils import Vector

OVERSIZE = 1.6                        # a real 4.0 x 1.9 x 1.2 m car, authored oversize
HL = 2.0 * OVERSIZE                   # half-length
HW = 0.92 * OVERSIZE                  # half-width at the widest station
Z0 = 0.42 * OVERSIZE                  # sill / ground clearance
ROOF_H = 0.78 * OVERSIZE              # roof height above the sill

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def new_object(name, mesh):
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(ob)
    return ob

def solid_primitive(name, verts_op, loc, rot=(0, 0, 0), scale=(1, 1, 1)):
    verts_op(location=loc, rotation=rot)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ob

def mirror(ob):
    m = ob.modifiers.new("mirror_y", 'MIRROR')
    m.use_axis = (False, True, False)
    m.use_bisect_axis = (False, False, False)
    m.use_mirror_merge = False   # the two sides never touch at Y=0; nothing to weld
    return ob

def ring(x, half_width, height):
    """Six points describing a rounded-roof half-box cross-section, open along the bottom:
    sill -- door -- shoulder -- roof -- shoulder -- door -- sill, mirrored across Y=0."""
    w, h = half_width, height
    return [
        (x, -w, Z0), (x, -w, Z0 + h * 0.7), (x, -w * 0.55, Z0 + h),
        (x, w * 0.55, Z0 + h), (x, w, Z0 + h * 0.7), (x, w, Z0),
    ]

clear()

# --- body: seven stations from tail to nose, each a ring, bridged into one shell.
stations = [
    (-HL, HW * 0.45, 0.06),
    (-HL * 0.82, HW * 0.85, 0.42),
    (-HL * 0.38, HW * 1.00, ROOF_H * 0.92),
    (HL * 0.05, HW * 0.98, ROOF_H),
    (HL * 0.48, HW * 0.82, 0.55),
    (HL * 0.82, HW * 0.55, 0.20),
    (HL, HW * 0.32, 0.05),
]
rings = [ring(x, w, h) for x, w, h in stations]

bm = bmesh.new()
vert_rings = [[bm.verts.new(p) for p in r] for r in rings]
bm.verts.ensure_lookup_table()
for a, b in zip(vert_rings, vert_rings[1:]):
    for i in range(len(a) - 1):
        bm.faces.new((a[i], a[i + 1], b[i + 1], b[i]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
body_mesh = bpy.data.meshes.new("body")
bm.to_mesh(body_mesh)
bm.free()
new_object("body", body_mesh)

# --- a belly panel under most of the cabin, not the whole underside (no full floor pan, as
# above): it blocks most rays looking up through that gap, not all of them. A real car has
# exactly this shape -- an under-engine skid plate -- for an unrelated reason.
# Sized to stay inside the body's sill width at every station it spans (the sill tapers
# toward nose and tail) -- a wider panel pokes past the hull as a visible sliver at the ends.
belly = bpy.data.meshes.new("belly")
belly.from_pydata([
    (-HL * 0.7, -HW * 0.6, Z0), (HL * 0.35, -HW * 0.6, Z0),
    (HL * 0.35, HW * 0.6, Z0), (-HL * 0.7, HW * 0.6, Z0),
], [], [(0, 1, 2, 3)])
belly.update()
new_object("belly_panel", belly)

# --- wheels, one pair built at +Y and mirrored: two cylinders, front and rear, on the ground
WHEEL_R, WHEEL_W = 0.33 * OVERSIZE, 0.22 * OVERSIZE
for name, x in (("wheel_front", HL * 0.68), ("wheel_rear", -HL * 0.68)):
    w = solid_primitive(name, bpy.ops.mesh.primitive_cylinder_add,
                         loc=(x, HW * 0.95, WHEEL_R), rot=(math.radians(90), 0, 0),
                         scale=(WHEEL_R, WHEEL_R, WHEEL_W))
    mirror(w)

# --- mostly hidden inside the shell and under the belly panel built above
engine = solid_primitive("engine_block", bpy.ops.mesh.primitive_cube_add,
                          loc=(-HL * 0.05, 0, Z0 + 0.18 * OVERSIZE), scale=(0.5 * OVERSIZE, HW * 0.45, 0.1 * OVERSIZE))

# --- a coincident duplicate: scan_defects' other real finding, same technique as
# make_demo_scene.py -- copy the object, link it, move nothing.
dup_src = bpy.data.objects["engine_block"]
dup = dup_src.copy(); dup.data = dup_src.data.copy()
dup.name = "Copy (1) of engine_block"
bpy.context.collection.objects.link(dup)

path = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else \
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "out", "demo_vehicle.blend")
os.makedirs(os.path.dirname(path), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)

objs = [o for o in bpy.data.objects if o.type == 'MESH']
pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
lo = [min(p[i] for p in pts) * 1000 for i in range(3)]
hi = [max(p[i] for p in pts) * 1000 for i in range(3)]
mods = sum(len(o.modifiers) for o in objs)
print("demo vehicle: %d objects  %d verts  %d unapplied modifiers  bbox mm X %.0f Y %.0f Z %.0f  -> %s"
      % (len(objs), sum(len(o.data.vertices) for o in objs), mods,
         hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], path))

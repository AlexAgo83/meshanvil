"""Generate a figurine-scale demonstration subject from primitives -- no donor file, nothing
to license, everything regenerates. A simple standing figure, authored at a real human
height so the size decision recenter records is doing real work, not a no-op, and with a
genuinely thin feature (fingers) for the thin-feature guard to have something to warn about
once the figure is remeshed down to a print size.

Every part is an individually closed primitive (sphere, cylinder, box); joining them without
welding leaves each one's own topology untouched, so the result has zero open edges and zero
non-manifold edges by construction -- sound on purpose, the same way make_demo_scene.py's
defects are planted on purpose.

    blender -b -P tools/make_demo_figure.py -- <destination.blend>
"""
import bpy, bmesh, os, sys, math

HEIGHT = 1.75                          # a real adult height, metres
FINGER_R = 0.008                       # 16 mm diameter -- ~1.6 mm once recentred to 180 mm

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def part(verts_op, loc, rot=(0, 0, 0), scale=(1, 1, 1), **kwargs):
    verts_op(location=loc, rotation=rot, **kwargs)
    ob = bpy.context.object
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ob

def half_capped(loc, rot, scale, open_end):
    """A cylinder capped at one end only: nothing sits near-tangent to the sphere embedding
    the open end, while the capped end stays a solid-looking limb rather than a visible pipe.
    A flat disk meeting a sphere anywhere but its own equator leaves a sliver behind at the
    crossing; the torso's top meets the head off-equator (open), its bottom meets the hip
    dead-on at the hip sphere's own equator (safe to cap)."""
    bpy.ops.mesh.primitive_cylinder_add(location=loc, rotation=rot, end_fill_type='NGON')
    ob = bpy.context.object
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    top = open_end == "top"
    doomed = [f for f in bm.faces if len(f.verts) > 4 and (f.calc_center_median().z > 0) == top]
    bmesh.ops.delete(bm, geom=doomed, context='FACES')
    bm.to_mesh(ob.data)
    bm.free()
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ob

clear()
parts = []

head_r = HEIGHT * 0.065
parts.append(part(bpy.ops.mesh.primitive_uv_sphere_add, loc=(0, 0, HEIGHT - head_r),
                   scale=(head_r, head_r, head_r)))

torso_h, torso_r = HEIGHT * 0.32, HEIGHT * 0.11
torso_top = HEIGHT - head_r * 1.6
parts.append(half_capped(loc=(0, 0, torso_top - torso_h / 2), rot=(0, 0, 0),
                          scale=(torso_r, torso_r * 0.65, torso_h / 2), open_end="top"))

hip_r = torso_r * 0.9
hip_z = torso_top - torso_h
parts.append(part(bpy.ops.mesh.primitive_uv_sphere_add, loc=(0, 0, hip_z),
                   scale=(hip_r, hip_r * 0.65, hip_r * 0.7)))

leg_r = HEIGHT * 0.045
foot_r = leg_r * 1.3
# The leg's bottom cap sits well inside the foot sphere (past its centre, not grazing its
# pole): a flat disk meeting a sphere near its pole leaves an arbitrarily thin sliver between
# them, which is exactly the kind of seam thin_feature_mm is built to catch -- just not the
# one this figure means to demonstrate.
leg_bottom = foot_r * 1.15
for side in (-1, 1):
    x = side * torso_r * 0.5
    leg_len = hip_z - leg_bottom
    parts.append(part(bpy.ops.mesh.primitive_cylinder_add, loc=(x, 0, leg_bottom + leg_len / 2),
                       scale=(leg_r, leg_r, leg_len / 2)))
    parts.append(part(bpy.ops.mesh.primitive_uv_sphere_add, loc=(x, HEIGHT * 0.03, foot_r),
                       scale=(foot_r * 1.6, foot_r * 2.2, foot_r)))

shoulder_z = torso_top - torso_h * 0.08
arm_len, arm_r = HEIGHT * 0.30, HEIGHT * 0.032
for side in (-1, 1):
    shoulder_x = side * torso_r * 0.95
    hand_x = side * (torso_r * 0.95 + arm_len * math.sin(math.radians(12)))
    hand_z = shoulder_z - arm_len * math.cos(math.radians(12))
    parts.append(part(bpy.ops.mesh.primitive_cylinder_add,
                       loc=((shoulder_x + hand_x) / 2, 0, (shoulder_z + hand_z) / 2),
                       rot=(0, side * math.radians(12), 0),
                       scale=(arm_r, arm_r, arm_len / 2)))

    # palm: a small flattened box at the wrist
    palm_len = HEIGHT * 0.045
    parts.append(part(bpy.ops.mesh.primitive_cube_add, loc=(hand_x, 0, hand_z - palm_len * 0.6),
                       scale=(arm_r * 0.95, arm_r * 0.55, palm_len)))

    # fingers: four thin parallel cylinders fanned from the palm -- the thin feature the
    # whole figurine demonstration exists to expose once this is remeshed at print size.
    finger_len = HEIGHT * 0.045
    for i in range(4):
        fy = (i - 1.5) * FINGER_R * 5.0   # gap wider than the finger itself, or the thin-feature
                                           # scanner (a ray finding the nearest opposite surface)
                                           # measures the gap between fingers, not a finger
        parts.append(part(bpy.ops.mesh.primitive_cylinder_add,
                           loc=(hand_x, fy, hand_z - palm_len * 1.1 - finger_len * 0.5),
                           scale=(FINGER_R, FINGER_R, finger_len / 2)))

bpy.ops.object.select_all(action='DESELECT')
for p in parts:
    p.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
figure = bpy.context.object
figure.name = "figure"

path = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else \
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "out", "demo_figure.blend")
os.makedirs(os.path.dirname(path), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)

from mathutils import Vector
pts = [figure.matrix_world @ Vector(c) for c in figure.bound_box]
lo = [min(p[i] for p in pts) * 1000 for i in range(3)]
hi = [max(p[i] for p in pts) * 1000 for i in range(3)]
print("demo figure: 1 object  %d verts  bbox mm X %.0f Y %.0f Z %.0f  finger diameter %.1f mm  -> %s"
      % (len(figure.data.vertices), hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], FINGER_R * 2000, path))

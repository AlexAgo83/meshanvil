"""Generate a subject whose thinnest feature is known exactly, for the guard checks.

Two subjects, each isolating one guard.

`guard_fixture.blend` is one closed box, 100 x 100 x 2 mm. Its smallest object extent is
100 mm and its thinnest feature is 2 mm, so the two measures cannot be confused by accident:
a check that passes on it is reading geometry, not bounding boxes.

`guard_pinhole.blend` is a closed sphere with a single face removed: a volume with a pinhole,
four boundary edges out of a thousand. A zero test calls it an open panel and walls it, which
hollows it -- the shape of the defect measured on a sculpt at 4 edges out of 29 600. The slab
cannot show that, because a perfectly closed body takes the branch that was always right.

That contrast is the whole point. The measure this fixture guards used to be the smallest
object's bounding extent, which on a subject that is one object returns the subject.

    blender -b -P tools/make_guard_fixture.py
"""
import bpy, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/work/out"

THICKNESS_MM = 2.0
SIDE_MM = 100.0

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
slab = bpy.context.object
slab.name = "slab"
# A cube added at size 1.0 spans one metre, so the scale is the target over 1000, not 2000.
slab.scale = (SIDE_MM / 1000.0, SIDE_MM / 1000.0, THICKNESS_MM / 1000.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/guard_fixture.blend", compress=True)
print("guard fixture: 1 object, %.0f x %.0f x %.1f mm, thinnest feature %.1f mm"
      % (SIDE_MM, SIDE_MM, THICKNESS_MM, THICKNESS_MM))

import bmesh

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, segments=32, ring_count=16)
ball = bpy.context.object
ball.name = "pinholed"
mesh = bmesh.new()
mesh.from_mesh(ball.data)
mesh.faces.ensure_lookup_table()
bmesh.ops.delete(mesh, geom=[mesh.faces[0]], context="FACES_ONLY")
boundary = sum(1 for e in mesh.edges if len(e.link_faces) == 1)
edges = len(mesh.edges)
mesh.to_mesh(ball.data)
ball.data.update()
mesh.free()

bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/guard_pinhole.blend", compress=True)
print("guard pinhole: 1 object, %d boundary edges of %d (%.2f%% open)"
      % (boundary, edges, 100.0 * boundary / edges))

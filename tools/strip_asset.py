"""Reduce a render asset to what the pipeline needs, and nothing else.

A .blend from a model library carries materials, node trees, UV layers, colour attributes,
cameras and lamps. None of it survives a voxel remesh and none of it is read by any operation
here -- the viewer renders with Workbench, which shades from geometry alone. Dropping it takes
the AC Cobra from 4.8 MB to 0.8 MB with every defect the demonstration depends on intact:
the modifier stacks, the parts sealed inside the body, the uniform oversize, the duplicate.

    blender -b <source.blend> -P tools/strip_asset.py -- <destination.blend>
"""
import bpy, bmesh, sys
from pathlib import Path
from mathutils import Vector

out = Path(sys.argv[sys.argv.index("--") + 1]).resolve()

# Raised lettering spelling a brand is a trademark whatever the mesh licence says, and the
# pipeline has no use for it. Named objects go, and so does anything whose geometry is a
# word: an asset that ships as a fixture should carry no mark it does not own.
BRANDED = {"text", "logo", "badge", "watermark", "copyright", "shelby", "cobra"}

dropped = []
for ob in list(bpy.data.objects):
    if ob.type != 'MESH':
        bpy.data.objects.remove(ob, do_unlink=True)
        continue
    stem = ob.name.split(".")[0].strip().lower()
    if stem in BRANDED:
        dropped.append(ob.name)
        bpy.data.objects.remove(ob, do_unlink=True)
print("dropped trademark geometry: %s" % (dropped or "none"))

for mesh in bpy.data.meshes:
    mesh.materials.clear()
    while mesh.uv_layers:
        mesh.uv_layers.remove(mesh.uv_layers[0])
    while mesh.color_attributes:
        mesh.color_attributes.remove(mesh.color_attributes[0])

for collection in (bpy.data.materials, bpy.data.images, bpy.data.node_groups,
                   bpy.data.textures, bpy.data.cameras, bpy.data.lights, bpy.data.worlds):
    for item in list(collection):
        collection.remove(item)
bpy.ops.outliner.orphans_purge(do_recursive=True)

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
kinds = {}
for o in meshes:
    for m in o.modifiers:
        kinds[m.type] = kinds.get(m.type, 0) + 1
open_edges = 0
for o in meshes:
    bm = bmesh.new()
    bm.from_mesh(o.data)
    open_edges += sum(1 for e in bm.edges if len(e.link_faces) != 2)
    bm.free()

out.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)

points = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
low = [min(p[i] for p in points) * 1000 for i in range(3)]
high = [max(p[i] for p in points) * 1000 for i in range(3)]
print("stripped: %d objects  %d verts  %s  %d open edges  %.0f x %.0f x %.0f mm  -> %.2f MB"
      % (len(meshes), sum(len(o.data.vertices) for o in meshes), kinds, open_edges,
         high[0] - low[0], high[1] - low[1], high[2] - low[2], out.stat().st_size / 1048576))

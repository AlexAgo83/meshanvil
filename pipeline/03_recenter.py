import bpy
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du depot
from mathutils import Vector
DIR = f"{ROOT}/work"
obs = [o for o in bpy.data.objects if o.type == 'MESH']
vs = [(o.matrix_world @ v.co, o) for o in obs for v in o.data.vertices]
lo = Vector([min(p[i] for p, _ in vs) for i in range(3)])
hi = Vector([max(p[i] for p, _ in vs) for i in range(3)])
print("avant: %.3f %.3f %.3f -> %.3f %.3f %.3f" % (*lo, *hi))
# centre en XY, pose sur z=0
delta = Vector((-(lo.x + hi.x)/2, -(lo.y + hi.y)/2, -lo.z))
for o in obs:
    o.location += delta
    o.select_set(True)
bpy.context.view_layer.objects.active = obs[0]
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
# origine de l'objet au centre de la geometrie
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
for o in obs: o.location = (0, 0, 0) if False else o.location
vs = [(o.matrix_world @ v.co) for o in obs for v in o.data.vertices]
lo = Vector([min(p[i] for p in vs) for i in range(3)])
hi = Vector([max(p[i] for p in vs) for i in range(3)])
print("apres: %.4f %.4f %.4f -> %.4f %.4f %.4f" % (*lo, *hi))
print("dims mm: %.1f x %.1f x %.1f" % tuple((hi[i]-lo[i])*1000 for i in range(3)))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.wm.stl_export(filepath=f"{DIR}/envelope_1-10.stl", global_scale=1000.0)
bpy.ops.wm.save_as_mainfile(filepath=f"{DIR}/envelope.blend")
print("reecrit")

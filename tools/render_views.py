import bpy
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du depot
from mathutils import Vector
sc = bpy.context.scene
ob = bpy.data.objects["ENVELOPPE"]
vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
lo = Vector([min(p[i] for p in vs) for i in range(3)])
hi = Vector([max(p[i] for p in vs) for i in range(3)])
ctr = (lo + hi) / 2
R = (hi - lo).length / 2
cam_d = bpy.data.cameras.new("c"); cam_d.type = 'ORTHO'; cam_d.ortho_scale = R * 2.3
# La camera recule de 4 rayons : son clipping se dimensionne sur le sujet, sinon la limite
# de 1000 unites de Blender avale une piece a l'echelle du millimetre et le rendu sort vide.
cam_d.clip_start, cam_d.clip_end = R * 1e-3, R * 10
cam = bpy.data.objects.new("c", cam_d)
sc.collection.objects.link(cam); sc.camera = cam
lt = bpy.data.lights.new("l", 'SUN'); lo2 = bpy.data.objects.new("l", lt)
sc.collection.objects.link(lo2); lo2.rotation_euler = (0.9, 0.2, 0.6)
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.resolution_x, sc.render.resolution_y = 1400, 900
for nom, d in (("3q", Vector((-1.1, -1.0, 0.55))), ("cote", Vector((0, -1, 0.05))),
               ("face", Vector((-1, 0, 0.05))), ("dessus", Vector((0.01, 0.01, 1)))):
    d = d.normalized()
    cam.location = ctr + d * R * 4
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = f"{ROOT}/work/renders/env_{nom}.png"
    bpy.ops.render.render(write_still=True)
print("rendus ok  dims mm: %.1f x %.1f x %.1f" % tuple((hi[i]-lo[i])*1000 for i in range(3)))

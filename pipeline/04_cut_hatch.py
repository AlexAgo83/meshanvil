import bpy, bmesh, sys
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du depot
from mathutils import Vector
DIR = f"{ROOT}/work/out"
# trappe rectangulaire dans le plancher, entre les appuis (mm)
X0, X1, Y0, Y1, ZTOP = -95, 95, -55, 55, 78
def log(*a): print("[tr]", *a); sys.stdout.flush()
def mesure(ob, tag):
    vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
    lo = [min(p[i] for p in vs) for i in range(3)]; hi = [max(p[i] for p in vs) for i in range(3)]
    bm = bmesh.new(); bm.from_mesh(ob.data)
    nm = sum(1 for e in bm.edges if len(e.link_faces) != 2); vol = bm.calc_volume(signed=True); bm.free()
    log("%-12s dims %.1f x %.1f x %.1f mm | vol %.1f cm3 | libres %d | faces %d"
        % (tag, *[(hi[i]-lo[i])*1000 for i in range(3)], vol*1e6, nm, len(ob.data.polygons)))
ob = bpy.data.objects["ENVELOPPE"]
bpy.context.view_layer.objects.active = ob
mesure(ob, "depart")
cx, cy, cz = (X0+X1)/2000, (Y0+Y1)/2000, (ZTOP-10)/2000
bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz))
box = bpy.context.object
box.scale = ((X1-X0)/1000, (Y1-Y0)/1000, (ZTOP+10)/1000)
bpy.ops.object.transform_apply(scale=True)
bpy.context.view_layer.objects.active = ob
m = ob.modifiers.new("b", 'BOOLEAN'); m.object = box; m.operation='DIFFERENCE'; m.solver='EXACT'
bpy.ops.object.modifier_apply(modifier=m.name)
bpy.data.objects.remove(box, do_unlink=True)
mesure(ob, "trappe")
bpy.ops.wm.save_as_mainfile(filepath=f"{DIR}/coque_trappe.blend")
bpy.ops.wm.stl_export(filepath=f"{DIR}/coque_trappe.stl", global_scale=1000.0)
log("ecrit coque_trappe.blend + .stl")

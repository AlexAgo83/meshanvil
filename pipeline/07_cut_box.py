import bpy, bmesh, sys
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du depot
from mathutils import Vector
DIR = f"{ROOT}/work/out"
X0, X1, Y0, Y1, Z0, Z1 = 105.5, 115.0, 29.0, 53.2, 23.5, 30.5   # mm, boite serree sur la tige
def log(*a): print("[eg]", *a); sys.stdout.flush()
ob = bpy.data.objects["ENVELOPPE"]; mw = ob.matrix_world
def dans(p): return (X0/1000 < p.x < X1/1000 and Y0/1000 < p.y < Y1/1000 and Z0/1000 < p.z < Z1/1000)
avant = sum(1 for v in ob.data.vertices if dans(mw @ v.co))
log("sommets dans la boite avant coupe:", avant)
bpy.context.view_layer.objects.active = ob
bpy.ops.mesh.primitive_cube_add(size=1, location=((X0+X1)/2000, (Y0+Y1)/2000, (Z0+Z1)/2000))
box = bpy.context.object
box.scale = ((X1-X0)/1000, (Y1-Y0)/1000, (Z1-Z0)/1000)
bpy.ops.object.transform_apply(scale=True)
bpy.context.view_layer.objects.active = ob
m = ob.modifiers.new("b", 'BOOLEAN'); m.object = box; m.operation='DIFFERENCE'; m.solver='EXACT'
bpy.ops.object.modifier_apply(modifier=m.name)
bpy.data.objects.remove(box, do_unlink=True)
apres = sum(1 for v in ob.data.vertices if dans(mw @ v.co))
bm = bmesh.new(); bm.from_mesh(ob.data)
vus, comps = set(), []
for v0 in bm.verts:
    if v0 in vus: continue
    pile, c = [v0], []; vus.add(v0)
    while pile:
        v = pile.pop(); c.append(v)
        for e in v.link_edges:
            w = e.other_vert(v)
            if w not in vus: vus.add(w); pile.append(w)
    comps.append(len(c))
nm = sum(1 for e in bm.edges if len(e.link_faces) != 2); vol = bm.calc_volume(signed=True); bm.free()
vs = [mw @ v.co for v in ob.data.vertices]
lo = [min(p[i] for p in vs) for i in range(3)]; hi = [max(p[i] for p in vs) for i in range(3)]
log("sommets dans la boite apres:", apres)
log("coques:", sorted(comps, reverse=True)[:6], "| total", len(comps))
log("dims %.1f x %.1f x %.1f mm | vol %.1f cm3 | libres %d | faces %d"
    % (*[(hi[i]-lo[i])*1000 for i in range(3)], vol*1e6, nm, len(ob.data.polygons)))
bpy.ops.wm.save_as_mainfile(filepath=f"{DIR}/coque_trappe.blend")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.wm.stl_export(filepath=f"{DIR}/coque_trappe.stl", global_scale=1000.0)
log("reecrit")

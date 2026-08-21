import bpy, bmesh, sys
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du depot
from mathutils import Vector
DIR = f"{ROOT}/work/out"
def log(*a): print("[p2]", *a); sys.stdout.flush()
def coques(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    vus, out = set(), []
    for v0 in bm.verts:
        if v0 in vus: continue
        pile, comp = [v0], []; vus.add(v0)
        while pile:
            v = pile.pop(); comp.append(v)
            for e in v.link_edges:
                w = e.other_vert(v)
                if w not in vus: vus.add(w); pile.append(w)
        out.append(comp)
    n = [len(c) for c in out]; bm.free(); return sorted(n, reverse=True)
ob = bpy.data.objects["ENVELOPPE"]
bpy.context.view_layer.objects.active = ob
log("coques au depart:", coques(ob))
# 1. jeter les pions horizontaux rates
bm = bmesh.new(); bm.from_mesh(ob.data)
vus, comps = set(), []
for v0 in bm.verts:
    if v0 in vus: continue
    pile, comp = [v0], []; vus.add(v0)
    while pile:
        v = pile.pop(); comp.append(v)
        for e in v.link_edges:
            w = e.other_vert(v)
            if w not in vus: vus.add(w); pile.append(w)
    comps.append(comp)
jetes = [v for c in comps if len(c) < 3000 for v in c]
if jetes: bmesh.ops.delete(bm, geom=jetes, context='VERTS'); log("pions rates jetes:", len(jetes), "sommets")
bm.to_mesh(ob.data); ob.data.update(); bm.free()
# 2. pions verticaux: appendice a 65.1, paroi a 73.4 -> on traverse de 60 a 78
for x, y in ((-0.0929, -0.0638), (-0.0928, 0.0639)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.003, depth=0.018,
                                        location=(x, y, 0.069))
    p = bpy.context.object
    bpy.context.view_layer.objects.active = ob
    m = ob.modifiers.new("u", 'BOOLEAN'); m.object = p; m.operation='UNION'; m.solver='EXACT'
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(p, do_unlink=True)
    log("pion vertical en (%.1f, %.1f) mm -> coques:" % (x*1000, y*1000), coques(ob))
bm = bmesh.new(); bm.from_mesh(ob.data)
nm = sum(1 for e in bm.edges if len(e.link_faces) != 2); vol = bm.calc_volume(signed=True); bm.free()
vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
lo = [min(p[i] for p in vs) for i in range(3)]; hi = [max(p[i] for p in vs) for i in range(3)]
log("dims %.1f x %.1f x %.1f mm | vol %.1f cm3 | libres %d | faces %d"
    % (*[(hi[i]-lo[i])*1000 for i in range(3)], vol*1e6, nm, len(ob.data.polygons)))
bpy.ops.wm.save_as_mainfile(filepath=f"{DIR}/coque_trappe.blend")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.wm.stl_export(filepath=f"{DIR}/coque_trappe.stl", global_scale=1000.0)
log("reecrit")

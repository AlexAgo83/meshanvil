import bpy, bmesh, sys
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du depot
from mathutils import Vector
DIR, SEUIL = f"{ROOT}/work/out", 3000
def log(*a): print("[net]", *a); sys.stdout.flush()
ob = bpy.data.objects["ENVELOPPE"]; mw = ob.matrix_world
bm = bmesh.new(); bm.from_mesh(ob.data)
vus, coques = set(), []
for v0 in bm.verts:
    if v0 in vus: continue
    pile, comp = [v0], []; vus.add(v0)
    while pile:
        v = pile.pop(); comp.append(v)
        for e in v.link_edges:
            w = e.other_vert(v)
            if w not in vus: vus.add(w); pile.append(w)
    coques.append(comp)
coques.sort(key=len, reverse=True)
jetes = [v for c in coques if len(c) < SEUIL for v in c]
log("coques: %d | supprimees: %d | sommets jetes: %d"
    % (len(coques), sum(1 for c in coques if len(c) < SEUIL), len(jetes)))
if jetes: bmesh.ops.delete(bm, geom=jetes, context='VERTS')
nm = sum(1 for e in bm.edges if len(e.link_faces) != 2)
vol = bm.calc_volume(signed=True)
bm.to_mesh(ob.data); ob.data.update(); bm.free()
vs = [mw @ v.co for v in ob.data.vertices]
lo = [min(p[i] for p in vs) for i in range(3)]; hi = [max(p[i] for p in vs) for i in range(3)]
log("apres: dims %.1f x %.1f x %.1f mm | vol %.1f cm3 | libres %d | faces %d"
    % (*[(hi[i]-lo[i])*1000 for i in range(3)], vol*1e6, nm, len(ob.data.polygons)))
bpy.ops.wm.save_as_mainfile(filepath=f"{DIR}/coque_trappe.blend")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.wm.stl_export(filepath=f"{DIR}/coque_trappe.stl", global_scale=1000.0)
log("reecrit")

import bpy, bmesh
from mathutils import Vector
ob = bpy.data.objects["ENVELOPPE"]; mw = ob.matrix_world
bm = bmesh.new(); bm.from_mesh(ob.data)
vus, coques = set(), []
for v0 in bm.verts:
    if v0 in vus: continue
    pile, comp = [v0], []
    vus.add(v0)
    while pile:
        v = pile.pop(); comp.append(v)
        for e in v.link_edges:
            w = e.other_vert(v)
            if w not in vus: vus.add(w); pile.append(w)
    coques.append(comp)
coques.sort(key=len, reverse=True)
print("coques:", len(coques))
for c in coques[:25]:
    ps = [mw @ v.co for v in c]
    lo = [min(p[i] for p in ps)*1000 for i in range(3)]; hi = [max(p[i] for p in ps)*1000 for i in range(3)]
    print("  %7d v  %6.1f..%6.1f  %6.1f..%6.1f  %6.1f..%6.1f   (%.0fx%.0fx%.0f mm)"
          % (len(c), lo[0],hi[0], lo[1],hi[1], lo[2],hi[2], hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2]))
if len(coques) > 25: print("  ... et", len(coques)-25, "autres")
petites = [c for c in coques[1:] if len(c) < 200]
print("coques de moins de 200 sommets:", len(petites))

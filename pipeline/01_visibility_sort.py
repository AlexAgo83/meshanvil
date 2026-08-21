"""Classe les objets d'une scene selon leur visibilite depuis l'exterieur.
Tir de rayons paralleles depuis N directions reparties sur une sphere."""
import bpy, json, math, sys
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du depot
from mathutils import Vector

N_DIR = 42          # directions (spirale de Fibonacci)
GRID  = 110         # rayons par cote et par direction
OUT   = f"{ROOT}/work/cache/visibility.json"

dg = bpy.context.evaluated_depsgraph_get()
sc = bpy.context.scene

pts = []
for o in bpy.data.objects:
    if o.type == 'MESH' and o.data.vertices:
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
ctr = (lo + hi) / 2
R = (hi - lo).length
print("bbox %.3f %.3f %.3f -> %.3f %.3f %.3f  R=%.3f" % (*lo, *hi, R))

def directions(n):
    d, ga = [], math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2*(i + 0.5)/n
        r = math.sqrt(max(0.0, 1 - z*z))
        t = ga * i
        d.append(Vector((r*math.cos(t), r*math.sin(t), z)))
    return d

vus = {}          # nom -> [hits totaux, hits depuis le dessus, hits depuis le dessous]
rays = 0
for k, d in enumerate(directions(N_DIR)):
    d.normalize()
    up = Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))
    u = d.cross(up).normalized()
    v = d.cross(u).normalized()
    demi = R / 2 * 1.05
    for i in range(GRID):
        a = (i + 0.5)/GRID * 2 - 1
        for j in range(GRID):
            b = (j + 0.5)/GRID * 2 - 1
            org = ctr + d*(R*0.75) + u*(a*demi) + v*(b*demi)
            ok, loc, nor, idx, ob, mat = sc.ray_cast(dg, org, -d, distance=R*2)
            rays += 1
            if ok and ob is not None:
                e = vus.setdefault(ob.name, [0, 0, 0])
                e[0] += 1
                if d.z > 0.35: e[1] += 1       # regard venant du dessus
                elif d.z < -0.35: e[2] += 1    # regard venant du dessous
    print("  direction %2d/%d  objets vus: %d" % (k+1, N_DIR, len(vus)))

meshes = [o.name for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
jamais = sorted(set(meshes) - set(vus))
json.dump({"vus": vus, "jamais": jamais, "rays": rays,
           "bbox": [list(lo), list(hi)]}, open(OUT, "w"), indent=1)
print("=== rayons tires: %d" % rays)
print("=== meshes: %d | vus: %d | jamais vus: %d" % (len(meshes), len(vus), len(jamais)))
tri = sorted(vus.items(), key=lambda kv: -kv[1][0])
print("--- 25 plus visibles ---")
for n, (t, h, b) in tri[:25]:
    print("  %6d  (dessus %5d / dessous %5d)  %s" % (t, h, b, n[-46:]))

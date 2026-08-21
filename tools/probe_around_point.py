import bpy
from mathutils import Vector
ob = bpy.data.objects["ENVELOPPE"]; mw = ob.matrix_world
C = Vector((0.1099, 0.0441, 0.0251))
for r in (0.006, 0.010, 0.015, 0.022):
    d = [mw @ v.co for v in ob.data.vertices if ((mw @ v.co) - C).length < r]
    if not d: print("r=%2.0fmm : rien" % (r*1000)); continue
    lo = [min(p[i] for p in d)*1000 for i in range(3)]; hi = [max(p[i] for p in d)*1000 for i in range(3)]
    print("r=%2.0fmm : %5d sommets  x %6.1f..%6.1f  y %5.1f..%5.1f  z %5.1f..%5.1f"
          % (r*1000, len(d), lo[0],hi[0], lo[1],hi[1], lo[2],hi[2]))
# profil en y le long de l'axe presume de la tige
print("--- coupe: sommets a moins de 5 mm de l'axe X passant par le curseur ---")
seg = [mw @ v.co for v in ob.data.vertices
       if abs((mw @ v.co).y - C.y) < 0.005 and abs((mw @ v.co).z - C.z) < 0.005]
xs = sorted(p.x*1000 for p in seg)
if xs: print("  %d sommets, x de %.1f a %.1f" % (len(xs), xs[0], xs[-1]))

import bpy
from mathutils import Vector
ob = bpy.data.objects["ENVELOPPE"]; mw = ob.matrix_world
vs = [mw @ v.co for v in ob.data.vertices]
for nom, C in (("AR droite (repere)", Vector(( 0.1099,  0.0441, 0.0251))),
               ("AR gauche",          Vector(( 0.1099, -0.0441, 0.0251))),
               ("AV droite",          Vector((-0.0929,  0.0441, 0.0251))),
               ("AV gauche",          Vector((-0.0929, -0.0441, 0.0251)))):
    d = [p for p in vs if (p - C).length < 0.008]
    if d:
        lo = [min(p[i] for p in d)*1000 for i in range(3)]; hi = [max(p[i] for p in d)*1000 for i in range(3)]
        print("%-20s %5d sommets  x %6.1f..%6.1f  y %6.1f..%6.1f  z %5.1f..%5.1f"
              % (nom, len(d), lo[0],hi[0], lo[1],hi[1], lo[2],hi[2]))
    else:
        print("%-20s rien dans un rayon de 8 mm" % nom)

import bpy
from mathutils import Vector
ob = bpy.data.objects["ENVELOPPE"]; mw = ob.matrix_world; mwi = mw.inverted()
up = (mwi.to_3x3() @ Vector((0,0,1))).normalized()
for nom, x, y in (("gauche", -0.0929, -0.0638), ("droite", -0.0928, 0.0639)):
    for dy in (0.0, -0.006, 0.006):
        org = mwi @ Vector((x, y+dy, 0.040))
        hits, p, g = [], org, 0
        while g < 12:
            ok, loc, nor, idx = ob.ray_cast(p, up, distance=0.20)
            if not ok: break
            hits.append((mw @ loc).z*1000); p = loc + up*0.0003; g += 1
        print("  %s dy=%+5.1fmm : %s" % (nom, dy*1000, " ".join("%.1f" % h for h in hits)))

import bpy, sys
from mathutils import Vector
f = sys.argv[-1]
ob = bpy.data.objects["ENVELOPPE"]; mw = ob.matrix_world
n = sum(1 for v in ob.data.vertices
        if (lambda p: abs(p.x) < 0.093 and abs(p.y) < 0.053 and -0.001 < p.z < 0.076)(mw @ v.co))
print("%s : %d sommets dans la zone de trappe" % (f, n))

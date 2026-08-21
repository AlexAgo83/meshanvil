"""Sweep a CAD-derived scene for export defects: smeared patches and coincident duplicates.
Read-only by default. Pass -- --fix to delete the exact duplicates and save.
Voir run_009_repair_export_defects_in_a_cad_derived_mesh."""
import bpy, sys, math, hashlib
from mathutils import Vector

FIX = "--fix" in sys.argv
obs = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]

def world_co(o):
    n = len(o.data.vertices); co = [0.0]*(3*n)
    o.data.vertices.foreach_get("co", co)
    mw = o.matrix_world
    return [mw @ Vector(co[3*i:3*i+3]) for i in range(n)]

# --- 1. smears: full bbox against the 5-95 percentile bbox
print("--- smear suspects (full extent / robust extent > 2.5)")
for o in obs:
    ps = world_co(o)
    if len(ps) < 8: continue
    if any(math.isnan(c) or math.isinf(c) for c in ps[0]):
        print("  NaN/inf  %s" % o.name); continue
    ax = [sorted(p[i] for p in ps) for i in range(3)]
    k = max(1, int(len(ps)*0.05))
    full = max(a[-1]-a[0] for a in ax)
    rob = max(a[-k-1]-a[k] for a in ax)
    if rob > 1e-9 and full/rob > 2.5 and full > 0.05:
        print("  x%-5.1f full %6.0f mm  robust %6.0f mm  %s" % (full/rob, full*1000, rob*1000, o.name[:60]))

# --- 2. duplicates: same counts + same world bbox, confirmed by coordinate hash
groups = {}
for o in obs:
    ps = [o.matrix_world @ Vector(c) for c in o.bound_box]
    key = (len(o.data.vertices), len(o.data.polygons)) + tuple(
        round(f(p[i] for p in ps), 5) for f in (min, max) for i in range(3))
    groups.setdefault(key, []).append(o)
dead, verts = [], 0
for k, v in groups.items():
    if len(v) < 2: continue
    byhash = {}
    for o in v:
        byhash.setdefault(hashlib.md5(b"".join(b"%.6f,%.6f,%.6f;" % tuple(p) for p in world_co(o))).hexdigest(), []).append(o)
    for same in byhash.values():
        dead += same[1:]; verts += (len(same)-1) * k[0]
print("--- coincident duplicates: %d redundant objects, %d vertices (%.1f%%)" % (
    len(dead), verts, 100*verts/sum(len(o.data.vertices) for o in obs)))

vs = [p for o in obs for p in (o.matrix_world @ Vector(c) for c in o.bound_box)]
lo = [min(p[i] for p in vs)*1000 for i in range(3)]; hi = [max(p[i] for p in vs)*1000 for i in range(3)]
print("scene: %d objects  %d verts  bbox X %.1f..%.1f Y %.1f..%.1f Z %.1f..%.1f" % (
    len(obs), sum(len(o.data.vertices) for o in obs), lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))

if FIX and dead:
    for o in dead: bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.wm.save_mainfile(compress=True)   # ponytail: compress, an uncompressed save was 2.5x the size
    print("removed %d duplicates, saved" % len(dead))

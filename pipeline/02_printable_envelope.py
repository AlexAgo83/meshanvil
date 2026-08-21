"""Enveloppe imprimable: tri -> solidify -> remesh voxel -> plus grosse coque -> STL."""
import bpy, bmesh, json, sys
import os; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du depot
from mathutils import Vector

GARDE   = set(json.load(open(f"{ROOT}/work/cache/envelope_parts.json")))
EPAIS   = 0.012      # solidify, metres reels (1.2 mm a 1/10)
VOXEL   = 0.008      # remesh, metres reels (0.8 mm a 1/10)
ECHELLE = 0.10       # 1/10
DIR     = f"{ROOT}/work"

def log(*a): print("[env]", *a); sys.stdout.flush()

# 0. figer les transformations AVANT toute suppression: supprimer un empty parent
#    fait sauter ses enfants a leur position locale.
fige = 0
for o in bpy.data.objects:
    if o.type == 'MESH' and o.name in GARDE and o.parent is not None:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
        fige += 1
log("parentages neutralises:", fige)

# 1. ne garder que l'enveloppe
bpy.ops.object.select_all(action='DESELECT')
sup = 0
for o in list(bpy.data.objects):
    if o.type != 'MESH' or o.name not in GARDE:
        bpy.data.objects.remove(o, do_unlink=True); sup += 1
log("objets supprimes:", sup, "| restants:", len(bpy.data.objects))

# 2. fusionner
objs = [o for o in bpy.data.objects if o.type == 'MESH']
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
bpy.ops.object.join()
ob = bpy.context.active_object
ob.name = "ENVELOPPE"
log("joint:", len(ob.data.vertices), "sommets,", len(ob.data.polygons), "faces")

# 2b. nettoyer avant d'epaissir: les faces degenerees font exploser le solidify en pics
bm = bmesh.new(); bm.from_mesh(ob.data)
n0 = len(bm.faces)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0002)
bmesh.ops.dissolve_degenerate(bm, dist=0.0002, edges=bm.edges)
bmesh.ops.triangulate(bm, faces=bm.faces)
bm.to_mesh(ob.data); ob.data.update(); bm.free()
log("nettoyage: %d -> %d faces" % (n0, len(ob.data.polygons)))

# 3. epaissir les surfaces ouvertes
m = ob.modifiers.new("solid", 'SOLIDIFY')
m.thickness = EPAIS; m.offset = 0
bpy.ops.object.modifier_apply(modifier=m.name)
log("apres solidify:", len(ob.data.polygons), "faces")

# 4. remesh voxel -> volume unique etanche
m = ob.modifiers.new("remesh", 'REMESH')
m.mode = 'VOXEL'; m.voxel_size = VOXEL; m.use_smooth_shade = False
bpy.ops.object.modifier_apply(modifier=m.name)
log("apres remesh:", len(ob.data.vertices), "sommets,", len(ob.data.polygons), "faces")

# 5. ne garder que la plus grosse coque
bm = bmesh.new(); bm.from_mesh(ob.data)
bm.verts.ensure_lookup_table()
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
log("coques:", len(coques), "| tailles:", [len(c) for c in coques])
# on garde toute coque significative (appendices detaches): seul le bruit part
SEUIL = 1000
for c in coques:
    xs = [v.co for v in c]
    log("   coque %6d sommets  bbox %s" % (len(c),
        " ".join("%.2f..%.2f" % (min(p[i] for p in xs), max(p[i] for p in xs)) for i in range(3))))
garde = [c for c in coques if len(c) >= SEUIL]
log("coques gardees:", len(garde), "/", len(coques))
if len(garde) < len(coques):
    perdus = [v for c in coques if len(c) < SEUIL for v in c]
    bmesh.ops.delete(bm, geom=perdus, context='VERTS')
    bm.to_mesh(ob.data); ob.data.update()
    log("ilots flottants supprimes:", len(perdus), "sommets")
bm.free()

# 6. controles
bm = bmesh.new(); bm.from_mesh(ob.data)
nm = sum(1 for e in bm.edges if len(e.link_faces) != 2)
vol = bm.calc_volume(signed=True)
bm.free()
vs = [ob.matrix_world @ v.co for v in ob.data.vertices]   # bound_box est perime apres bmesh
dim = [max(p[i] for p in vs) - min(p[i] for p in vs) for i in range(3)]
log("aretes non-manifold:", nm)
log("volume: %.2f L reel -> %.1f cm3 imprime" % (vol*1000, vol*1e6*ECHELLE**3))
log("cotes imprimees: %.1f x %.1f x %.1f mm" % tuple(d*ECHELLE*1000 for d in dim))

# 7. mise a l'echelle + export
ob.scale = (ECHELLE,)*3
bpy.ops.object.transform_apply(scale=True)
bpy.ops.wm.stl_export(filepath=f"{DIR}/envelope_1-10.stl", global_scale=1000.0)
bpy.ops.wm.save_as_mainfile(filepath=f"{DIR}/envelope.blend")
log("ecrit: envelope_1-10.stl + envelope.blend")

"""Genere une scene de demonstration: un boitier symetrique, deux enjoliveurs,
quatre appuis, plus deux defauts d'export reels -- un ilot etire et des objets
exactement superposes. Sert de fixture publique: rien de client, rien de binaire
a committer, tout se regenere.

    blender -b -P tools/make_demo_scene.py
"""
import bpy, bmesh, os, math
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/work/out"

def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def solid(name, verts_op, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    verts_op(location=loc, rotation=rot)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return ob

def shade(ob, level=2):
    m = ob.modifiers.new("b", 'BEVEL'); m.width = 0.004; m.segments = 2
    s = ob.modifiers.new("s", 'SUBSURF'); s.levels = level; s.render_levels = level
    bpy.context.view_layer.objects.active = ob
    for mod in (m.name, s.name):
        bpy.ops.object.modifier_apply(modifier=mod)

clear()
# --- corps: un boitier allonge
body = solid("housing_body", bpy.ops.mesh.primitive_cube_add, loc=(0, 0, 0.09), scale=(0.26, 0.13, 0.07))
shade(body, 2)

# --- capot: une voute posee dessus
hood = solid("housing_hood", bpy.ops.mesh.primitive_cylinder_add, loc=(0, 0, 0.15),
             rot=(0, math.radians(90), 0), scale=(0.06, 0.115, 0.24))
shade(hood, 2)

# --- quatre appuis cylindriques
for i, (x, y) in enumerate(((-0.19, -0.11), (-0.19, 0.11), (0.19, -0.11), (0.19, 0.11))):
    f = solid(f"foot_{i+1}", bpy.ops.mesh.primitive_cylinder_add, loc=(x, y, 0.03),
              scale=(0.028, 0.028, 0.032))
    shade(f, 1)

# --- deux enjoliveurs symetriques a l'avant, chacun en plusieurs ilots
def trim(side, sign):
    parts = []
    shell = solid(f"trim_shell_{side}", bpy.ops.mesh.primitive_cube_add,
                  loc=(-0.235, sign * 0.075, 0.105), scale=(0.03, 0.045, 0.038))
    shade(shell, 2); parts.append(shell)
    for j, dz in enumerate((-0.018, 0.018)):
        lens = solid(f"trim_lens_{side}_{j}", bpy.ops.mesh.primitive_uv_sphere_add,
                     loc=(-0.256, sign * 0.075, 0.105 + dz), scale=(0.012, 0.016, 0.016))
        parts.append(lens)
    ring = solid(f"trim_ring_{side}", bpy.ops.mesh.primitive_torus_add,
                 loc=(-0.252, sign * 0.075, 0.105), rot=(0, math.radians(90), 0))
    ring.scale = (0.042, 0.042, 0.042)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    parts.append(ring)
    # les ilots d'un enjoliveur forment un seul objet, comme dans un export tessele
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts: p.select_set(True)
    bpy.context.view_layer.objects.active = shell
    bpy.ops.object.join()
    shell.name = f"trim_{side}"
    return shell

trim_l = trim("L", -1)
trim_r = trim("R", 1)

# --- defaut 1: un ilot du cote droit etire le long d'une droite, comme a l'export
bm = bmesh.new(); bm.from_mesh(trim_r.data)
seen, comps = set(), []
for v0 in bm.verts:
    if v0 in seen: continue
    stack, comp = [v0], []; seen.add(v0)
    while stack:
        v = stack.pop(); comp.append(v)
        for e in v.link_edges:
            w = e.other_vert(v)
            if w not in seen: seen.add(w); stack.append(w)
    comps.append(comp)
comps.sort(key=len)
target = comps[0]                      # le plus petit ilot: une lentille
# Calibre sur le defaut observe en vrai: la trainee vaut environ 4x la piece,
# et un tiers des sommets de l'ilot part, le reste tient en place.
drift = Vector((2.4, -3.1, 1.0)).normalized() * 0.42
ordered = sorted(target, key=lambda v: v.co.x)
moved = 0
for k, v in enumerate(ordered):
    if k % 3: continue
    v.co += drift * (k / max(1, len(ordered) - 1))
    moved += 1
bm.to_mesh(trim_r.data); trim_r.data.update(); bm.free()
print("defect 1: %d of %d verts of one island smeared on trim_R" % (moved, len(target)))

# --- defaut 2: des objets exactement superposes
dups = 0
for name in ("housing_hood", "foot_2", "foot_3", "trim_L"):
    src = bpy.data.objects[name]
    cp = src.copy(); cp.data = src.data.copy()
    cp.name = f"Copy (1) of {name}"
    bpy.context.collection.objects.link(cp)
    dups += 1
print("defect 2: %d coincident duplicates" % dups)

os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=f"{OUT}/demo_source.blend", compress=True)
obs = [o for o in bpy.data.objects if o.type == 'MESH']
vs = [o.matrix_world @ Vector(c) for o in obs for c in o.bound_box]
lo = [min(p[i] for p in vs) * 1000 for i in range(3)]
hi = [max(p[i] for p in vs) * 1000 for i in range(3)]
print("demo scene: %d objects  %d verts  bbox X %.1f..%.1f Y %.1f..%.1f Z %.1f..%.1f"
      % (len(obs), sum(len(o.data.vertices) for o in obs), lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))

"""Sweep a CAD-derived scene for export defects: smeared patches and coincident duplicates.
Read-only by default. Pass -- --fix to delete the exact duplicates and save.
Voir run_009_repair_export_defects_in_a_cad_derived_mesh.

Runs standalone (prints, as it always did) or under `meshanvil run scan_defects <file>`,
which hands it a job and collects a report."""
import bpy, sys, os, math, hashlib
from mathutils import Vector

def _reporter():
    """The job carries the repository root; nothing is installed into Blender's interpreter."""
    if "--job" not in sys.argv:
        return None, {}
    import json
    from pathlib import Path
    args = sys.argv[sys.argv.index("--") + 1:]
    job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
    sys.path.insert(0, job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job

REPORT, JOB = _reporter()
PARAMS = (JOB or {}).get("params", {})


def _views():
    """Rendering lives in the engine module; a standalone run finds it beside this file."""
    from pathlib import Path
    sys.path.insert(0, (JOB or {}).get("root") or str(Path(__file__).resolve().parent.parent))
    from meshanvil_engine import views
    return views


views = _views()
FIX = bool(PARAMS.get("fix")) if REPORT else ("--fix" in sys.argv)
RATIO = float(PARAMS.get("smear_ratio_threshold", 2.5))
RENDER = bool(PARAMS.get("render", True))
MIN_EXTENT = float(PARAMS.get("min_extent_mm", 50.0)) / 1000.0
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
        print("  NaN/inf  %s" % o.name)
        if REPORT: REPORT.finding("non_finite_coordinates", subject=o.name)
        continue
    ax = [sorted(p[i] for p in ps) for i in range(3)]
    k = max(1, int(len(ps)*0.05))
    full = max(a[-1]-a[0] for a in ax)
    rob = max(a[-k-1]-a[k] for a in ax)
    if rob > 1e-9 and full/rob > RATIO and full > MIN_EXTENT:
        print("  x%-5.1f full %6.0f mm  robust %6.0f mm  %s" % (full/rob, full*1000, rob*1000, o.name[:60]))
        if REPORT:
            REPORT.finding("smeared_island", subject=o.name, ratio=round(full/rob, 2),
                           full_extent_mm=round(full*1000, 1), robust_extent_mm=round(rob*1000, 1))

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
share = verts / max(1, sum(len(o.data.vertices) for o in obs))
print("--- coincident duplicates: %d redundant objects, %d vertices (%.1f%%)" % (
    len(dead), verts, 100*share))
if REPORT and dead:
    REPORT.finding("coincident_duplicates", objects=len(dead), vertices=verts,
                   share_of_vertices=round(share, 3))

vs = [p for o in obs for p in (o.matrix_world @ Vector(c) for c in o.bound_box)]
lo = [min(p[i] for p in vs)*1000 for i in range(3)]; hi = [max(p[i] for p in vs)*1000 for i in range(3)]
print("scene: %d objects  %d verts  bbox X %.1f..%.1f Y %.1f..%.1f Z %.1f..%.1f" % (
    len(obs), sum(len(o.data.vertices) for o in obs), lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.measured(reporting.measure_scene())
    REPORT.warn("thin_parts_below_ray_grid")
    REPORT.cites("run_009_repair_export_defects_in_a_cad_derived_mesh")

if FIX and dead:
    for o in dead: bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.wm.save_mainfile(compress=True)   # ponytail: compress, an uncompressed save was 2.5x the size
    print("removed %d duplicates, saved" % len(dead))
    if REPORT:
        REPORT.output(bpy.data.filepath)
        REPORT.report["kind"] = "transform"

if RENDER and REPORT:
    from pathlib import Path as _Path
    views.shoot(REPORT, JOB, _Path(JOB["root"]), _Path(bpy.data.filepath).stem)

if REPORT:
    REPORT.write()

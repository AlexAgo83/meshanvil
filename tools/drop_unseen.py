"""Delete what ray_visibility never saw, so the outer envelope is all that is left.

ray_visibility only sorts; without this the operator has to leave the chain to act on its
verdict, and the most destructive step of the run is the one step with no report.
The grid lets a thin part fall through and come out "never seen" although it is visible,
so the bbox is checked afterwards: dropping an unseen object must not move the outer extent.
Voir run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility.
"""
import bpy, sys, json
from pathlib import Path


def _reporter():
    if "--job" not in sys.argv:
        return None, {}
    args = sys.argv[sys.argv.index("--") + 1:]
    job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
    # The package ships with the tool; the project only holds work.
    sys.path.insert(0, job.get("install") or job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job


REPORT, JOB = _reporter()


def _views():
    sys.path.insert(0, (JOB or {}).get("install") or (JOB or {}).get("root")
                    or str(Path(__file__).resolve().parent.parent))
    from meshanvil_engine import views
    return views


views = _views()
PARAMS = (JOB or {}).get("params", {})
FAINT_MAX = int(PARAMS.get("faint_max", 0))
RENDER = bool(PARAMS.get("render", True))
OUT = Path(bpy.data.filepath).with_name(Path(bpy.data.filepath).stem + "_visible.blend")
ROOT = Path((JOB or {}).get("root", Path(__file__).resolve().parent.parent))

# ray_visibility writes beside the work directory, under the name of the file it read.
CACHE = Path(PARAMS.get("cache") or "") if PARAMS.get("cache") else (
    Path(bpy.data.filepath).parent.parent / "cache"
    / (Path(bpy.data.filepath).stem + "_visibility.json"))

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.before(reporting.measure_scene())

if not CACHE.exists():
    message = "no visibility cache at %s: run ray_visibility first" % CACHE
    if REPORT:
        REPORT.failed(message)
        REPORT.write()
    sys.exit(message)

cache = json.loads(CACHE.read_text(encoding="utf-8"))
seen = cache.get("seen", {})
drop = set(cache.get("never", [])) | {n for n, hits in seen.items() if hits <= FAINT_MAX}

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
doomed = [o for o in meshes if o.name in drop]
# The names are read now: removing an object invalidates every reference to it.
doomed_names = sorted(o.name for o in doomed)
kept = len(meshes) - len(doomed)
print("[drop_unseen] meshes %d | dropping %d | keeping %d (faint_max %d)"
      % (len(meshes), len(doomed), kept, FAINT_MAX))

if kept == 0:
    message = "every mesh is unseen: refusing to empty the scene"
    if REPORT:
        REPORT.failed(message)
        REPORT.write()
    sys.exit(message)

for obj in doomed:
    bpy.data.objects.remove(obj, do_unlink=True)

if RENDER:
    views.shoot(REPORT, JOB, ROOT, OUT.stem)

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)

if REPORT:
    REPORT.after(reporting.measure_scene())
    REPORT.report["params"]["cache"] = str(CACHE)
    REPORT.report["params"]["dropped"] = len(doomed)
    REPORT.report["params"]["kept"] = kept
    REPORT.finding("dropped_unseen", dropped=len(doomed), kept=kept,
                   never_seen=len(cache.get("never", [])), faint_max=FAINT_MAX,
                   examples=doomed_names[:5])
    # An object nothing saw from outside cannot be holding the outer extent: if the bbox
    # moves, the grid missed a thin visible part and this dropped real skin.
    delta = REPORT.report.get("bbox_delta_mm") or {"axes_moved": []}
    if delta["axes_moved"]:
        REPORT.warn("bbox_moved_while_dropping_unseen")
    REPORT.cites("run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility")
    REPORT.output(str(OUT))
    REPORT.write()

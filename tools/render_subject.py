"""Render the subject from the standard views and record them, changing nothing.

Every transform already renders what it produced, so the one thing the chain could not do
was *look* at a file: shaping a generated asset meant rendering it outside the chain, with
no report and nothing in the viewer. This is that missing step -- an inspection whose whole
output is the four views a silhouette is judged on.

Voir run_012_build_a_recognizable_low_poly_subject_from_primitives, which says plainly that
nothing but a render confirms a shape reads as what it is meant to be.
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
# Workbench renders one flat grey by default, which cannot show whether a cut-out landed
# where it was meant to. If the subject carries materials, use them.
MATERIALS = bool(PARAMS.get("materials", True))
ROOT = Path((JOB or {}).get("root", Path(__file__).resolve().parent.parent))

meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
if not meshes:
    message = "nothing to render: the file holds no mesh with geometry"
    if REPORT:
        REPORT.failed(message)
        REPORT.write()
    sys.exit(message)

if MATERIALS and any(o.data.materials for o in meshes):
    bpy.context.scene.display.shading.color_type = 'MATERIAL'

stem = Path(bpy.data.filepath).stem
views.shoot(REPORT, JOB, ROOT, stem)

print("[render_subject] %d meshes, %d materials"
      % (len(meshes), len({m.name for o in meshes for m in o.data.materials if m})))

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.measured(reporting.measure_scene())
    REPORT.finding("rendered", objects=len(meshes),
                   materials=sorted({m.name for o in meshes for m in o.data.materials if m}),
                   views=len(REPORT.report.get("renders", [])))
    REPORT.cites("run_012_build_a_recognizable_low_poly_subject_from_primitives")
    REPORT.write()

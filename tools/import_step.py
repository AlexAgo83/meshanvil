"""Read a STEP source headlessly and export its tessellated mesh as STL."""
import json, math, sys, time
from pathlib import Path

import FreeCAD as App
import Import, MeshPart, Part

args = sys.argv[sys.argv.index("--") + 1:]
job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
params, source = job["params"], Path(job["target"])
report_path, progress = Path(job["report"]), Path(job["progress"])
out = Path(job["root"]) / "work" / "out" / (source.stem + "_step.stl")

def beat(step, fraction):
    progress.parent.mkdir(parents=True, exist_ok=True)
    progress.write_text(json.dumps({"at": time.time(), "step": step, "fraction": fraction}) + "\n", encoding="utf-8")

beat("reading STEP", .1)
document = App.newDocument("meshanvil_step")
Import.insert(str(source), document.Name)
# Part:: only. A STEP assembly imports as its solids *plus* an App::Part that contains them
# and an origin of three datum lines and three datum planes. Kept, the container hands the
# tessellator every solid twice, and the datums -- which are infinite -- turned the reported
# bounding box into 1e100 on every real assembly. The fixture, a lone box, never showed it.
objects = [obj for obj in document.Objects
           if obj.TypeId.startswith("Part::") and hasattr(obj, "Shape") and not obj.Shape.isNull()]
beat("tessellating", .6)
linear, angular = float(params["linear_deflection_mm"]), math.radians(float(params["angular_deflection_deg"]))
out.parent.mkdir(parents=True, exist_ok=True)
mesh = MeshPart.meshFromShape(Shape=Part.makeCompound([obj.Shape for obj in objects]),
                              LinearDeflection=linear, AngularDeflection=angular)
mesh.write(str(out), "STL")
bounds = [obj.Shape.BoundBox for obj in objects]
low = [min(getattr(box, axis + "Min") for box in bounds) for axis in "XYZ"]
high = [max(getattr(box, axis + "Max") for box in bounds) for axis in "XYZ"]
beat("writing report", .9)
report = {"schema_version": job["schema_version"], "id": job["id"], "chain": job["parent"] or job["id"],
          "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "kind": job["kind"],
          "operation": job["operation"], "script": job["script"], "engine": "freecad", "status": "ok",
          "params": params, "tool": job["tool"], "input": {"path": str(source), "sha256": job["input_sha256"], "mode": "read_only"},
          "findings": [{"code": "step_solids", "count": sum(len(obj.Shape.Solids) for obj in objects),
                        "bodies": len(objects)}],
          "measured": {"objects": len(objects), "vertices": None, "faces": None, "shells": len(objects),
                       "non_manifold_edges": None, "volume_cm3": None, "bbox_mm": {"min": low, "max": high}},
          "output": {"path": str(out), "sha256": None, "state": "present", "state_changed_at": None},
          "warnings": [], "links": {"parent": job["parent"], "parent_source": job["parent_source"], "docs": []}}
report_path.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")

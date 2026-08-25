"""Rebuild the reference table as solids and write it as STEP.

A mesh converted to STEP is a STEP file full of triangles: it opens, and it is useless to
anyone who wanted CAD -- no faces to select, no fillet to edit, no dimension to change. So
this does not convert the Blender table. It rebuilds the same design from the same numbers
(tools/table_dimensions.py) as six B-rep solids, which is what STEP is for.

The consequence is stated in the report rather than hidden: the target file is never read.
It anchors the chain and nothing more.

Runs under `meshanvil run make_table_step <anything>`.
"""
import json, sys, time
from pathlib import Path

import FreeCAD as App
import Import, Part

args = sys.argv[sys.argv.index("--") + 1:]
JOB = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
sys.path.insert(0, JOB.get("install") or JOB["root"])
from meshanvil_engine import report as reporting
from tools import table_dimensions

REPORT = reporting.Reporter(JOB)
PARAMS = JOB["params"]
PLAN = table_dimensions.layout(
    length=float(PARAMS["length_mm"]), width=float(PARAMS["width_mm"]),
    height=float(PARAMS["height_mm"]), shelf_fraction=float(PARAMS["shelf_fraction"]))
OUT = Path(JOB["root"]) / "work" / "out" / (Path(JOB["target"]).stem + ".step")


def slab(size_x, size_y, thick, top_z, corner):
    """A rounded rectangle as a solid: fillet the four upright edges, then soften the rest.

    The softening is attempted, not required. A fillet that cannot be built on some future
    set of dimensions must not cost the file -- the slab without it is still the right slab.
    """
    box = Part.makeBox(size_x, size_y, thick,
                       App.Vector(-size_x / 2, -size_y / 2, top_z - thick))
    upright = [e for e in box.Edges
               if abs(e.Vertexes[0].Point.z - e.Vertexes[1].Point.z) > 1e-9]
    shape = box.makeFillet(corner, upright)
    try:
        return shape.makeFillet(PLAN["ease"], shape.Edges)
    except Part.OCCError:
        REPORT.warn("edge_softening_not_applied")
        return shape


def leg(shoulder, foot):
    axis = App.Vector(foot[0] - shoulder[0], foot[1] - shoulder[1], foot[2] - shoulder[2])
    return Part.makeCone(PLAN["leg_top"], PLAN["leg_foot"], axis.Length,
                         App.Vector(*shoulder), App.Vector(axis).normalize())


REPORT.progress("building solids", 0.3)
parts = [slab(PLAN["length"], PLAN["width"], PLAN["top_thick"], PLAN["height"], PLAN["corner"]),
         slab(PLAN["shelf_x"], PLAN["shelf_y"], PLAN["shelf_thick"], PLAN["shelf_z"],
              PLAN["shelf_corner"])]
parts += [leg(shoulder, foot) for shoulder, foot in PLAN["legs"]]

REPORT.progress("writing STEP", 0.8)
document = App.newDocument("meshanvil_table")
for name, shape in zip(("top", "shelf", "leg_0", "leg_1", "leg_2", "leg_3"), parts):
    feature = document.addObject("Part::Feature", name)
    feature.Shape = shape
OUT.parent.mkdir(parents=True, exist_ok=True)
Import.export(document.Objects, str(OUT))

# Shape.BoundBox is OCC's cheap box and it is inflated on a filleted solid -- it put this
# 1100 mm top at 1114.8. optimalBoundingBox() is the one that agrees with the geometry.
box = Part.makeCompound(parts).optimalBoundingBox()
REPORT.measured({"objects": len(parts), "vertices": None, "faces": sum(len(s.Faces) for s in parts),
                 "shells": len(parts), "non_manifold_edges": None,
                 "volume_cm3": round(sum(s.Volume for s in parts) / 1000.0, 3),
                 "bbox_mm": {"min": [round(v, 3) for v in (box.XMin, box.YMin, box.ZMin)],
                             "max": [round(v, 3) for v in (box.XMax, box.YMax, box.ZMax)]}})
REPORT.finding("solids", count=len(parts), faces=sum(len(s.Faces) for s in parts),
               length_mm=round(PLAN["length"]), width_mm=round(PLAN["width"]),
               height_mm=round(PLAN["height"]))
# Declared, not implied: nothing of the target was read, and no comparison against the mesh
# table was made. Both come from the same plan; that they still agree is unverified here.
REPORT.warn("target_not_read")
REPORT.warn("not_compared_to_mesh_table")
# Same reference in the preview as the mesh branch: this branch is judged against the
# photograph too, and neither engine can do that judging.
REPORT.render("reference", JOB["target"], "photograph, not a render")
REPORT.output(str(OUT))
REPORT.write()

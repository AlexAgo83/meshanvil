"""Read a mesh interchange file into the chain, with a report behind it.

A subject that arrives as OBJ or STL cannot enter otherwise: the only other import reads STEP
through FreeCAD. Converting it by hand works and leaves nothing -- no fingerprint of the
source, no counts, no parent -- so the chain starts with an artefact nobody can trace.

The engine does not open the target: it is not a scene. The job carries the path, this script
imports it into an empty file, and the report records what came in and what was written.

Runs under `meshanvil run import_mesh <file>`.
Voir run_009_repair_export_defects_in_a_cad_derived_mesh.
"""
import bpy, sys
from pathlib import Path


def _reporter():
    """The job carries the repository root; nothing is installed into the engine's interpreter."""
    import sys, json
    from pathlib import Path
    if "--job" not in sys.argv:
        return None, {}
    args = sys.argv[sys.argv.index("--") + 1:]
    job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
    # The package ships with the tool; the project only holds work.
    sys.path.insert(0, job.get("install") or job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job


REPORT, JOB = _reporter()
PARAMS = (JOB or {}).get("params", {})
SOURCE = Path((JOB or {}).get("target", ""))
OUT = Path((JOB or {}).get("root", ".")) / "work" / "out" / (SOURCE.stem + "_imported.blend")

# Only what this project has a real source for. A format matrix nobody can test is worse than
# a refusal that names what it accepts.
READERS = {
    ".obj": lambda path: bpy.ops.wm.obj_import(filepath=path),
    ".stl": lambda path: bpy.ops.wm.stl_import(filepath=path),
    ".ply": lambda path: bpy.ops.wm.ply_import(filepath=path),
}


def log(*parts):
    print("[import]", *parts)
    sys.stdout.flush()


suffix = SOURCE.suffix.lower()
if suffix not in READERS:
    raise SystemExit("cannot read %s; this operation accepts %s"
                     % (suffix or "a file with no extension", ", ".join(sorted(READERS))))

bpy.ops.wm.read_factory_settings(use_empty=True)
if REPORT:
    REPORT.progress("reading", 0.2)
READERS[suffix](str(SOURCE))

meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
if not meshes:
    raise SystemExit("%s carried no mesh; nothing was written" % SOURCE.name)
log("read %s | objects %d | vertices %d"
    % (SOURCE.name, len(meshes), sum(len(o.data.vertices) for o in meshes)))

if REPORT:
    REPORT.progress("writing", 0.8)
OUT.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)

if REPORT:
    from meshanvil_engine import report as reporting
    measured = reporting.measure_scene()
    REPORT.measured(measured)
    REPORT.report["params"]["source_format"] = suffix
    REPORT.report["params"]["source_name"] = SOURCE.name
    REPORT.finding("imported", objects=measured["objects"], vertices=measured["vertices"],
                   faces=measured["faces"], source_format=suffix)
    # An interchange file carries no unit. What the numbers mean is the operator's to decide,
    # and recenter is where that decision gets recorded.
    REPORT.warn("units_not_declared_by_source")
    REPORT.cites("run_009_repair_export_defects_in_a_cad_derived_mesh")
    REPORT.output(str(OUT))
    REPORT.write()

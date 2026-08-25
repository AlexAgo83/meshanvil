"""Read a group of reference images as one source, and write the plan they were read into.

The operation a chain needs when a subject comes from more than one image. `run` takes a
single target, so the group is named by a list file -- one image per line, resolved beside it
-- and that list is the file the report declares, hashes and chains from. Every image in it is
hashed too, so a plan states which files it was read from and a changed screenshot shows up as
a plan that no longer matches.

It reads the images the way the rest of this project reads a photograph: it does not. The
reading is the work of whoever wrote tools/<subject>_reading.py, and what this operation
guarantees is only that the reading is recorded against the exact files it was made from.

It runs under Blender for one reason: `run` knows two engines and both are 3D applications.
Nothing here touches bpy, and the boot is the whole cost of the operation.
"""
import hashlib, importlib, json, sys
from pathlib import Path


def _reporter():
    args = sys.argv[sys.argv.index("--") + 1:]
    job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
    sys.path.insert(0, job.get("install") or job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job


REPORT, JOB = _reporter()
PARAMS = JOB["params"]
LIST = Path(JOB["target"])
OUT = Path(JOB["root"]) / "work" / "out" / (LIST.stem + "_plan.json")


def fingerprint(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


REPORT.progress("reading the list", 0.2)
names = [line.strip() for line in LIST.read_text(encoding="utf-8").splitlines()
         if line.strip() and not line.startswith("#")]
missing = [n for n in names if not (LIST.parent / n).is_file()]
if not names or missing:
    message = ("the list names no image" if not names
               else "missing beside %s: %s" % (LIST.name, ", ".join(missing)))
    REPORT.failed(message)
    REPORT.write()
    sys.exit(message)

REPORT.progress("fingerprinting", 0.6)
references = [{"name": n, "path": str((LIST.parent / n).resolve()),
               "sha256": fingerprint(LIST.parent / n)} for n in names]

subject = str(PARAMS["subject"]).strip()
if not subject:
    message = "no subject: pass --set subject=<name>, which names tools/<name>_reading.py"
    REPORT.failed(message)
    REPORT.write()
    sys.exit(message)
try:
    reading = importlib.import_module("tools.%s_reading" % subject)
except ModuleNotFoundError:
    message = "no reading for subject %r: expected tools/%s_reading.py" % (subject, subject)
    REPORT.failed(message)
    REPORT.write()
    sys.exit(message)
plan = reading.plan(references)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")

REPORT.sources([{"path": r["path"], "sha256": r["sha256"], "role": v["view"]}
                for r, v in zip(references, plan["references"])])
REPORT.finding("references", count=len(references),
               views=[r["view"] for r in plan["references"]],
               unrecognised=plan["unrecognised_references"])
if plan["unrecognised_references"]:
    REPORT.warn("reference_not_accounted_for")
# The images are the input and no engine opened them: a person read them, and the plan is that
# reading written down. Nothing here measured anything.
REPORT.warn("images_not_read_by_any_engine")
REPORT.warn("dimensions_declared_not_measured")
for reference in references:
    REPORT.render(reference["name"].replace("reference_%s_" % subject, ""),
                  reference["path"], "screenshot, not a render")
REPORT.output(str(OUT))
REPORT.write()

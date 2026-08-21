"""The only writer of an operation report.

Standard library plus the engine's own modules. An operation launched without a job still runs:
the reporter degrades to printing, which is what the twelve scripts did before it existed.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

SCHEMA_VERSION = 1
EMPTY = {"objects": None, "vertices": None, "faces": None, "shells": None,
         "non_manifold_edges": None, "volume_cm3": None, "bbox_mm": None}


def job_from_argv() -> dict | None:
    """--job <path> after the -- separator, as the runner passes it."""
    if "--" not in sys.argv or "--job" not in sys.argv:
        return None
    arguments = sys.argv[sys.argv.index("--") + 1:]
    path = Path(arguments[arguments.index("--job") + 1])
    return json.loads(path.read_text(encoding="utf-8"))


def measure_scene() -> dict:
    """Cheap, whole-scene. Everything an operation did not measure stays null, never zero."""
    import bpy
    from mathutils import Vector
    meshes = [o for o in bpy.data.objects if o.type == "MESH" and o.data.vertices]
    measured = dict(EMPTY)
    measured["objects"] = len(meshes)
    measured["vertices"] = sum(len(o.data.vertices) for o in meshes)
    measured["faces"] = sum(len(o.data.polygons) for o in meshes)
    points = [o.matrix_world @ v.co for o in meshes for v in o.data.vertices]
    if points:
        measured["bbox_mm"] = {
            "min": [round(min(p[i] for p in points) * 1000, 3) for i in range(3)],
            "max": [round(max(p[i] for p in points) * 1000, 3) for i in range(3)],
        }
    return measured


def measure_object(name: str) -> dict:
    """Full, one object: adds shells, non-manifold edges and volume."""
    import bpy, bmesh
    from mathutils import Vector
    ob = bpy.data.objects[name]
    mesh = bmesh.new()
    mesh.from_mesh(ob.data)
    seen, shells = set(), 0
    for start in mesh.verts:
        if start in seen:
            continue
        shells += 1
        stack = [start]
        seen.add(start)
        while stack:
            vertex = stack.pop()
            for edge in vertex.link_edges:
                other = edge.other_vert(vertex)
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
    measured = dict(EMPTY)
    measured["objects"] = 1
    measured["vertices"] = len(ob.data.vertices)
    measured["faces"] = len(ob.data.polygons)
    measured["shells"] = shells
    measured["non_manifold_edges"] = sum(1 for e in mesh.edges if len(e.link_faces) != 2)
    measured["volume_cm3"] = round(mesh.calc_volume(signed=True) * 1e6, 3)
    mesh.free()
    points = [ob.matrix_world @ v.co for v in ob.data.vertices]
    measured["bbox_mm"] = {
        "min": [round(min(p[i] for p in points) * 1000, 3) for i in range(3)],
        "max": [round(max(p[i] for p in points) * 1000, 3) for i in range(3)],
    }
    return measured


def bbox_delta(before: dict, after: dict) -> dict | None:
    """The comparison the runbooks call the check that caught every failure. Computed here, so
    no operation can forget it."""
    if not (before.get("bbox_mm") and after.get("bbox_mm")):
        return None
    low = [round(after["bbox_mm"]["min"][i] - before["bbox_mm"]["min"][i], 3) for i in range(3)]
    high = [round(after["bbox_mm"]["max"][i] - before["bbox_mm"]["max"][i], 3) for i in range(3)]
    moved = [axis for i, axis in enumerate("XYZ") if abs(low[i]) > 1e-3 or abs(high[i]) > 1e-3]
    return {"min": low, "max": high, "axes_moved": moved}


class Reporter:
    """Opened at the start of an operation, closed at the end, whatever happened."""

    def __init__(self, job: dict | None):
        self.job = job
        self.started = time.time()
        self.report = {
            "schema_version": SCHEMA_VERSION,
            "id": (job or {}).get("id"),
            "chain": None,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "kind": (job or {}).get("kind", "inspection"),
            "operation": (job or {}).get("operation"),
            "script": (job or {}).get("script"),
            "engine": (job or {}).get("engine", "blender"),
            "status": "ok",
            "params": (job or {}).get("params", {}),
            "tool": {**(job or {}).get("tool", {}),
                     "engine_python": sys.version.split()[0]},
            "input": {"path": (job or {}).get("target"),
                      "sha256": (job or {}).get("input_sha256"), "mode": "read_only"},
            "warnings": [],
            "renders": [],
            "findings": [],
            "links": {"parent": (job or {}).get("parent"),
                      "parent_source": (job or {}).get("parent_source"), "docs": []},
        }

    # --- what an operation calls ---------------------------------------------------------
    def before(self, measured: dict) -> None:
        self.report["before"] = measured

    def after(self, measured: dict) -> None:
        self.report["after"] = measured
        self.report["bbox_delta_mm"] = bbox_delta(self.report.get("before", {}), measured)

    def measured(self, measured: dict) -> None:
        self.report["measured"] = measured

    def finding(self, code: str, **fields) -> None:
        self.report["findings"].append({"code": code, **fields})

    def warn(self, code: str) -> None:
        if code not in self.report["warnings"]:
            self.report["warnings"].append(code)

    def render(self, view: str, path: str, camera: str, tile: bool = False) -> None:
        self.report["renders"].append({"view": view, "path": path, "camera": camera, "tile": tile})

    def cites(self, *docs: str) -> None:
        self.report["links"]["docs"].extend(docs)

    def output(self, path: str, sha256: str | None = None) -> None:
        self.report["output"] = {"path": path, "sha256": sha256,
                                 "state": "present", "state_changed_at": None}
        self.report["input"]["mode"] = "copy"

    def progress(self, step: str, fraction: float | None = None) -> None:
        """A long operation proving it is alive. Transient, and never part of the report."""
        line = json.dumps({"at": time.time(), "step": step, "fraction": fraction})
        print(f"[progress] {step}" + (f" {fraction:.0%}" if fraction is not None else ""))
        if self.job:
            with open(self.job["progress"], "a", encoding="utf-8") as handle:
                handle.write(line + "\n")

    def failed(self, error: str) -> None:
        self.report["status"] = "failed"
        self.report["error"] = error

    # --- closing -------------------------------------------------------------------------
    def write(self) -> None:
        self.report["duration_s"] = round(time.time() - self.started, 2)
        for key in ("findings", "renders"):
            if not self.report[key]:
                self.report.pop(key)
        if not self.job:
            print(json.dumps(self.report, indent=1))
            return
        self.report["chain"] = self.report["links"]["parent"] or self.report["id"]
        Path(self.job["report"]).write_text(
            json.dumps(self.report, indent=1) + "\n", encoding="utf-8")


def open_report() -> Reporter:
    return Reporter(job_from_argv())

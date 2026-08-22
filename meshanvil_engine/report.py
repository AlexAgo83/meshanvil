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


def thin_feature_mm(objects=None, samples: int = 2000, percentile: float = 0.02,
                    floor_mm: float | None = None) -> dict:
    """How thin the thinnest part of a body is, measured through the geometry.

    The measure this replaces was the smallest object's bounding extent, which answers a
    different question: on a subject that is one object it returns the whole subject. A
    180 mm figurine reported 180 mm while a 1.5 mm voxel was fusing its fingers, because a
    finger is not an object.

    This casts a ray from each sampled face straight into the body and takes the distance to
    the far wall. On a closed body that distance is the local thickness; the low percentile
    of it is the thinnest feature a voxel has to survive.

    A hit only counts as a far wall when it faces away from the ray. Without that test the
    measure reads gaps instead of solids: between two fingers, or across an open mouth, the
    ray lands immediately on a surface pointing back at it and the estimate collapses to
    microns. Measured on a 180 mm figurine, the unfiltered version returned 0.002 mm.

    It is an estimate: it samples, it only sees what a ray from a face centre reaches, and on
    an open surface there is no far wall at all -- those samples are dropped, so a body of
    open panels reports nothing rather than a number that means something else.
    """
    import bpy
    from mathutils import Vector

    objects = objects if objects is not None else [
        o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
    faces = [(o, i) for o in objects for i in range(len(o.data.polygons))]
    if not faces:
        return {"thin_feature_mm": None, "median_mm": None, "samples": 0,
                "share_below_floor": None, "estimate": True}
    stride = max(1, len(faces) // max(1, samples))
    depths = []
    for o, index in faces[::stride]:
        polygon = o.data.polygons[index]
        inward = -Vector(polygon.normal)
        if inward.length_squared < 1e-12:
            continue
        inward.normalize()
        # Start just inside the surface, or the ray hits the face it was cast from.
        origin = Vector(polygon.center) + inward * 1e-5
        hit, location, normal, _ = o.ray_cast(origin, inward)
        if not hit or normal.length_squared < 1e-12:
            continue
        if normal.normalized().dot(inward) < 0.5:
            continue          # a facing surface across a gap, not the far side of a solid
        # Local units are not millimetres when the object carries a scale.
        span = (o.matrix_world @ location) - (o.matrix_world @ origin)
        depths.append(span.length)
    if not depths:
        return {"thin_feature_mm": None, "median_mm": None, "samples": 0,
                "share_below_floor": None, "estimate": True}
    depths.sort()
    rank = min(len(depths) - 1, int(len(depths) * percentile))
    # The thinnest sample says a feature exists; the share says how much of the body is in
    # that state. On a subject whose fine trim is far below the voxel the first number warns
    # every time, and only the second tells a reader whether that matters here.
    share = None
    if floor_mm is not None:
        share = round(sum(1 for d in depths if d * 1000 < floor_mm) / len(depths), 4)
    return {"thin_feature_mm": round(depths[rank] * 1000, 3),
            "median_mm": round(depths[len(depths) // 2] * 1000, 3),
            "samples": len(depths), "share_below_floor": share, "estimate": True}


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
            "comparisons": [],
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

    def comparison(self, view: str, before: str, after: str, camera: str) -> None:
        self.report["comparisons"].append({"view": view, "before": before, "after": after,
                                            "camera": camera})

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
        for key in ("findings", "renders", "comparisons"):
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

"""Join every mesh and remesh it at a voxel size: the step that turns an assembly into one solid.

Runs standalone or under `meshanvil run voxel_remesh <file> --set voxel_mm=6`.
Voir run_006_turn_a_cad_assembly_into_a_printable_solid.
"""
import bpy, sys, json
from pathlib import Path


def _reporter():
    if "--job" not in sys.argv:
        return None, {}
    args = sys.argv[sys.argv.index("--") + 1:]
    job = json.loads(Path(args[args.index("--job") + 1]).read_text(encoding="utf-8"))
    sys.path.insert(0, job["root"])
    from meshanvil_engine import report as reporting
    return reporting.open_report(), job


REPORT, JOB = _reporter()
PARAMS = (JOB or {}).get("params", {})
VOXEL = float(PARAMS.get("voxel_mm", 6.0)) / 1000.0
KEEP_LARGEST = bool(PARAMS.get("keep_largest", False))
DRIFT = float(PARAMS.get("max_bbox_drift_mm", 0.0)) or float(PARAMS.get("voxel_mm", 6.0))
OUT = Path(bpy.data.filepath).with_name(
    Path(bpy.data.filepath).stem + "_voxel%g.blend" % (VOXEL * 1000))


def log(*parts):
    print("[remesh]", *parts)
    sys.stdout.flush()


meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]
if not meshes:
    raise SystemExit("no mesh in this file")

# The smallest part decides what a voxel can keep: anything thinner than one voxel is erased,
# which is the trap run_006 records and no topology check ever reports.
smallest = min(max((max(p[i] for p in (o.matrix_world @ v.co for v in o.data.vertices))
                    - min(p[i] for p in (o.matrix_world @ v.co for v in o.data.vertices)))
                   for i in range(3)) for o in meshes)
log("objects %d | smallest extent %.1f mm | voxel %.1f mm"
    % (len(meshes), smallest * 1000, VOXEL * 1000))

if REPORT:
    REPORT.progress("joining", 0.1)
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.join()
envelope = bpy.context.object
envelope.name = "ENVELOPPE"
before_data = envelope.data.copy() if REPORT and bool(PARAMS.get("render", True)) else None
before_object = None
if before_data:
    before_object = bpy.data.objects.new("ENVELOPPE_BEFORE", before_data)
    bpy.context.scene.collection.objects.link(before_object)
    before_object.matrix_world = envelope.matrix_world.copy()
    before_object.hide_render = True

if REPORT:
    from meshanvil_engine import report as reporting
    REPORT.before(reporting.measure_object("ENVELOPPE"))
    REPORT.progress("remeshing", 0.4)

modifier = envelope.modifiers.new("r", 'REMESH')
modifier.mode = 'VOXEL'
modifier.voxel_size = VOXEL
bpy.ops.object.modifier_apply(modifier=modifier.name)

if KEEP_LARGEST:
    import bmesh
    mesh = bmesh.new()
    mesh.from_mesh(envelope.data)
    seen, parts = set(), []
    for start in mesh.verts:
        if start in seen:
            continue
        stack, part = [start], []
        seen.add(start)
        while stack:
            vertex = stack.pop()
            part.append(vertex)
            for edge in vertex.link_edges:
                other = edge.other_vert(vertex)
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        parts.append(part)
    parts.sort(key=len, reverse=True)
    dropped = [v for part in parts[1:] for v in part]
    if dropped:
        bmesh.ops.delete(mesh, geom=dropped, context='VERTS')
        log("kept the largest of %d shells, dropped %d vertices" % (len(parts), len(dropped)))
    mesh.to_mesh(envelope.data)
    envelope.data.update()
    mesh.free()

if REPORT:
    REPORT.progress("measuring", 0.8)
    after = reporting.measure_object("ENVELOPPE")
    REPORT.after(after)
    REPORT.report["params"]["smallest_input_extent_mm"] = round(smallest * 1000, 1)
    if smallest < VOXEL:
        REPORT.warn("features_below_voxel_erased")
    delta = REPORT.report.get("bbox_delta_mm") or {"min": [0, 0, 0], "max": [0, 0, 0]}
    drift = max(abs(v) for v in delta["min"] + delta["max"])
    if drift > DRIFT:
        REPORT.warn("bbox_drift_beyond_tolerance")
        REPORT.failed("bounding box moved by %.1f mm, tolerance is %.1f mm" % (drift, DRIFT))
    REPORT.cites("run_006_turn_a_cad_assembly_into_a_printable_solid")

RENDER = bool(PARAMS.get("render", True))
if RENDER:
    from mathutils import Vector
    if REPORT:
        REPORT.progress("rendering", 0.9)
    points = [envelope.matrix_world @ v.co for v in envelope.data.vertices]
    if before_object:
        points += [before_object.matrix_world @ v.co for v in before_object.data.vertices]
    low = Vector([min(p[i] for p in points) for i in range(3)])
    high = Vector([max(p[i] for p in points) for i in range(3)])
    centre, radius = (low + high) / 2, (high - low).length / 2
    scene = bpy.context.scene
    camera_data = bpy.data.cameras.new("c"); camera_data.type = 'ORTHO'
    camera_data.ortho_scale = radius * 2.3
    camera = bpy.data.objects.new("c", camera_data)
    scene.collection.objects.link(camera); scene.camera = camera
    sun = bpy.data.objects.new("l", bpy.data.lights.new("l", 'SUN'))
    scene.collection.objects.link(sun); sun.rotation_euler = (0.9, 0.2, 0.6)
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.background_type = 'VIEWPORT'
    scene.display.shading.background_color = (0.094, 0.094, 0.094)
    scene.render.resolution_x, scene.render.resolution_y = 1200, 760
    renders = Path(OUT).parent.parent / "renders"
    renders.mkdir(parents=True, exist_ok=True)
    for name, direction in (("3q", Vector((-1.1, -1.0, 0.55))), ("front", Vector((-1, 0, 0.1))),
                            ("side", Vector((0, -1, 0.1))), ("top", Vector((0.01, 0.01, 1)))):
        unit = direction.normalized()
        camera.location = centre + unit * radius * 4
        camera.rotation_euler = (-unit).to_track_quat('-Z', 'Y').to_euler()
        identity = (JOB or {}).get("id", "standalone")
        path = renders / f"{identity}_{Path(OUT).stem}_{name}.png"
        scene.render.filepath = str(path); bpy.ops.render.render(write_still=True)
        if REPORT:
            REPORT.render(name, str(path), "ortho-%s-object" % name, tile=(name == "3q"))
        if before_object:
            envelope.hide_render, before_object.hide_render = True, False
            before_path = renders / f"{identity}_{Path(OUT).stem}_before_{name}.png"
            scene.render.filepath = str(before_path); bpy.ops.render.render(write_still=True)
            envelope.hide_render, before_object.hide_render = False, True
            if REPORT:
                REPORT.comparison(name, str(before_path), str(path), "ortho-%s-subject" % name)
    log("rendered 4 views")

bpy.ops.wm.save_as_mainfile(filepath=str(OUT), compress=True)
log("wrote", OUT.name)
if REPORT:
    REPORT.output(str(OUT))
    REPORT.write()

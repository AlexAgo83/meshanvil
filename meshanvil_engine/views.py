"""Four canonical directions, on a camera framed once and never moved.

Two states are only comparable if the camera did not move between them, so the frame is
computed from the union of both states before either is shot. That is the whole reason this
lives in one place instead of in each operation: a camera fitted per state makes a wipe lie.

An operation that changes geometry says so with a number and shows it with a render. The
render confirms; it does not establish. See adr_001 and run_006.
"""
from __future__ import annotations

import bpy
from mathutils import Vector

DIRECTIONS = (("3q", Vector((-1.1, -1.0, 0.55))), ("front", Vector((-1, 0, 0.1))),
              ("side", Vector((0, -1, 0.1))), ("top", Vector((0.01, 0.01, 1))))
WIDTH, HEIGHT = 1200, 760
TILE = "3q"


def meshes():
    return [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices]


def _points(objects):
    return [o.matrix_world @ v.co for o in objects for v in o.data.vertices]


def _fit(points, centre):
    """The ortho width that holds the subject from every canonical direction.

    One width for all four views and for both states, because a camera fitted per view or per
    state makes a wipe lie -- but fitted against what is actually projected, not against the
    bounding diagonal. `ortho_scale` sizes the *long* sensor axis, so on a 1200x760 frame the
    visible height is 0.63 of it: a 432 mm hammer under the old diagonal rule was given 352 mm
    of height and was cropped at both ends, while a car, being wide, never showed the bug.
    """
    need = 0.0
    for _, direction in DIRECTIONS:
        rotation = (-direction.normalized()).to_track_quat('-Z', 'Y')
        right, up = rotation @ Vector((1, 0, 0)), rotation @ Vector((0, 1, 0))
        across = [(p - centre).dot(right) for p in points]
        upward = [(p - centre).dot(up) for p in points]
        need = max(need, max(across) - min(across),
                   (max(upward) - min(upward)) * WIDTH / HEIGHT)
    return max(need * 1.12, 1e-4)


def _stage(points):
    """One ortho camera and one sun, framed on every point it will ever be pointed at."""
    low = Vector([min(p[i] for p in points) for i in range(3)])
    high = Vector([max(p[i] for p in points) for i in range(3)])
    centre, radius = (low + high) / 2, max((high - low).length / 2, 1e-4)

    scene = bpy.context.scene
    data = bpy.data.cameras.new("meshanvil_cam")
    data.type = 'ORTHO'
    data.ortho_scale = _fit(points, centre)
    camera = bpy.data.objects.new("meshanvil_cam", data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    sun = bpy.data.objects.new("meshanvil_sun", bpy.data.lights.new("meshanvil_sun", 'SUN'))
    scene.collection.objects.link(sun)
    sun.rotation_euler = (0.9, 0.2, 0.6)

    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.background_type = 'VIEWPORT'
    scene.display.shading.background_color = (0.094, 0.094, 0.094)
    scene.render.resolution_x, scene.render.resolution_y = WIDTH, HEIGHT
    # The scene decides the extension. A source saved with JPEG output writes .jpg beside a
    # report claiming .png: the render exists and the viewer shows a hole.
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False
    return camera, centre, radius


def shoot(report, job, root, stem, subjects=None, before=None):
    """Render `subjects` from every direction, and `before` from the same camera if given.

    Returns nothing: what it produced is recorded in the report, which is the only place
    anything downstream reads. A render that did not land where the report says stops the
    operation rather than leaving a path pointing at nothing.
    """
    subjects = subjects if subjects is not None else [o for o in meshes() if o not in (before or [])]
    if not subjects:
        return
    camera, centre, radius = _stage(_points(subjects) + _points(before or []))

    folder = root / "work" / "renders"
    folder.mkdir(parents=True, exist_ok=True)
    identity = (job or {}).get("id", "standalone")
    scene = bpy.context.scene

    def expose(shown, hidden, path):
        for o in hidden:
            o.hide_render = True
        for o in shown:
            o.hide_render = False
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        if not path.is_file():
            raise SystemExit(f"render was not written where the report says: {path}")

    for index, (name, direction) in enumerate(DIRECTIONS):
        if report:
            report.progress("rendering", 0.9 + 0.09 * index / len(DIRECTIONS))
        unit = direction.normalized()
        camera.location = centre + unit * radius * 4
        camera.rotation_euler = (-unit).to_track_quat('-Z', 'Y').to_euler()

        after_path = folder / f"{identity}_{stem}_{name}.png"
        expose(subjects, before or [], after_path)
        if report:
            report.render(name, str(after_path), f"ortho-{name}-object", tile=(name == TILE))

        if before:
            before_path = folder / f"{identity}_{stem}_before_{name}.png"
            expose(before, subjects, before_path)
            if report:
                report.comparison(name, str(before_path), str(after_path), f"ortho-{name}-subject")

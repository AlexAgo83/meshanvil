"""The reference table's numbers, in millimetres, in one place.

Two builders read this: Blender models the table as a mesh, FreeCAD rebuilds it as solids for
STEP. They share the geometry because two copies of these numbers drift apart on the first
change, and the drift is invisible -- both files still produce a table.

Plain arithmetic, no engine imported, so either interpreter can read it.
"""

LENGTH, WIDTH, HEIGHT = 1100.0, 600.0, 400.0
SHELF_FRACTION = 0.55                   # of the height; the photograph puts it a little over half
TOP_THICK, SHELF_THICK = 30.0, 18.0
CORNER, EASE = 90.0, 4.0                # the top's corner radius, and the softening on every edge
LEG_TOP, LEG_FOOT = 24.0, 16.0          # leg radii, top and foot
SPLAY_X, SPLAY_Y = 55.0, 40.0           # how far each foot stands outside its own shoulder
INSET_X, INSET_Y = 110.0, 70.0          # where a leg meets the top, in from that corner


def layout(length=LENGTH, width=WIDTH, height=HEIGHT, shelf_fraction=SHELF_FRACTION):
    """Every derived dimension, from the four a caller is allowed to change."""
    shelf_z = height * shelf_fraction
    # The shelf clears the legs it hangs between, so it is inset by where they have leaned to
    # at its own height -- it is not simply a smaller copy of the top.
    lean = 1 - shelf_z / height
    legs = []
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        shoulder = (sx * (length / 2 - INSET_X), sy * (width / 2 - INSET_Y), height - TOP_THICK)
        run = (sx * SPLAY_X, sy * SPLAY_Y)
        # A leaning leg ends in a tilted disc, so its lower rim reaches below the point the leg
        # is aimed at -- the first table stood 3 mm into the floor. Aim that much higher and the
        # rim, which is what actually touches, lands on z = 0 with the height still the height
        # that was asked for. One correction, not iterated: the residual is 22 microns.
        drop = shoulder[2]
        span = (run[0] ** 2 + run[1] ** 2) ** 0.5
        dip = LEG_FOOT * span / (span ** 2 + drop ** 2) ** 0.5
        legs.append((shoulder, (shoulder[0] + run[0], shoulder[1] + run[1], dip)))
    return {
        "length": length, "width": width, "height": height,
        "top_thick": TOP_THICK, "shelf_thick": SHELF_THICK,
        "corner": CORNER, "shelf_corner": CORNER * 0.7, "ease": EASE,
        "leg_top": LEG_TOP, "leg_foot": LEG_FOOT,
        "shelf_z": shelf_z,
        "shelf_x": length - 2 * (INSET_X - LEG_TOP - SPLAY_X * lean),
        "shelf_y": width - 2 * (INSET_Y - LEG_TOP - SPLAY_Y * lean),
        "legs": legs,
    }


def demo():
    """One check: the table stands on the floor and is as tall as it was asked to be."""
    plan = layout()
    for shoulder, foot in plan["legs"]:
        span = ((foot[0] - shoulder[0]) ** 2 + (foot[1] - shoulder[1]) ** 2) ** 0.5
        length = (span ** 2 + (shoulder[2] - foot[2]) ** 2) ** 0.5
        # The rim of the tilted foot, which is what touches, within a tenth of a millimetre.
        rim = foot[2] - LEG_FOOT * span / length
        assert abs(rim) < 0.1, rim
        assert shoulder[2] == HEIGHT - TOP_THICK
    assert plan["shelf_x"] < plan["length"] and plan["shelf_y"] < plan["width"]
    assert 0 < plan["shelf_z"] < plan["height"]
    print("table_dimensions ok:", {k: round(v, 1) for k, v in plan.items() if isinstance(v, float)})


if __name__ == "__main__":
    demo()

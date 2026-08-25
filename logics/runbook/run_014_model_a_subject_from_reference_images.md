## run_014_model_a_subject_from_reference_images - Model a subject from reference images
> Status: Active
> Category: other
> Verified: 2026-08-25 (a coffee table from one photograph, two render-led iterations, and a city car from two CAD screenshots, four; the table chain also produced the 3 mm floor penetration that no render showed and `bbox_mm` did)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- A subject arrives as a picture -- a photograph, a screenshot, a catalogue shot -- and there is no 3D file behind it.
- Someone asks whether the tool "does image to 3D".

# The honest answer to that question
There is no reconstruction here, and there is none coming from a single image: one picture
carries no depth, and nothing can recover what was never in it. What works is the other
direction, and it is the loop this whole project is built on. A person or an agent **reads**
the image, **writes a generator** from primitives, **renders** it, **looks** at the render
against the image, and corrects. See run_012 for the generator craft itself; this runbook is
only about what changes when the brief is a picture.

Say that before starting. "It will resemble it" and "it will be it" are different promises,
and the second one cannot be kept.

# What an image decides, and what it never does
| The image decides | The image says nothing about |
|---|---|
| the silhouette and the plan (a rectangle, or a coke-bottle waist) | any dimension at all |
| which surfaces are which (glass, panel, tyre) | wall thickness, material, tolerance |
| where features sit *relative to each other* | where they sit in millimetres |
| the character: leg splay, tail rake, corner radius | whether the real object is symmetric |

So **every size is a declared parameter, not a measurement**, and the reports must say so.
The coffee table is 1100 x 600 x 400 mm because that is *a* coffee table, not because anyone
measured *that* coffee table. Someone who has the real one measures it and passes the numbers:

```bash
meshanvil run make_table work/in/reference_table.png --set length_mm=1250 --set height_mm=380
```

# One view or several
One view gives an outline and leaves the other axis to invention. Two three-quarters, front
and rear, pin what a side elevation cannot: on the city car they gave the plan (a rectangle,
no waist anywhere), both fascias, and a windscreen base at 650 mm from the centre -- the
cab-forward proportion of the class, and the thing that would have been guessed wrong from a
profile alone.

If a second view exists, use it. If only one does, say which half of the model is invention.

# Procedure
1. **Put the images in the project**, under `work/in/`, and name them for what they show:
   `reference_<subject>_front.png`, `reference_<subject>_rear.png`.
2. **Declare the group as a group.** `run` takes one target, so a list file -- one image per
   line, resolved beside it -- is what the chain declares and hangs from:
   `meshanvil run read_references work/in/<subject>_references.txt --set subject=<subject>`.
   It fingerprints every image, so a plan states which files it was read from and a changed
   screenshot shows up later as a plan that no longer matches.
3. **Keep the reading as data**, in `tools/<subject>_reading.py`: which view contributed what,
   and the tables that reading produced. The generator then builds from the plan and opens
   nothing else -- an input it actually reads, and a parent that is the reading.
4. **Build, render, look, correct.** Nothing else validates this. Budget several passes: two
   for a table, four for a car.
5. **Put the reference in the preview.** Both operations list the images in `renders[]`, so
   the screenshot sits in the same panel as the render. The comparison no engine can make
   should not also require going to find the file.
6. **Declare what was not checked.** `images_not_read_by_any_engine` and
   `dimensions_declared_not_measured` on the reading; `not_compared_to_reference_images` on
   the model. Those warnings are the point: they are true, and they stay true.

# What the render catches, and what only the numbers do
The render is the check -- and it is not the only one. On the first table every render looked
right and `bbox_mm.min.z` read **-2.892**: the table stood 3 mm inside the floor, because a
leaning leg ends in a tilted disc whose lower rim reaches below the point the leg was aimed
at. Nothing visible at any camera angle. Aim the foot higher by that much and the rim, which
is what actually touches, lands on z = 0 with the height still the height that was asked for.

Read the measurements after every pass, not only the pictures. Voir run_010.

# Defects this loop found, in order
Each was invisible in the numbers and obvious in a render, or the reverse.
1. **A glass band that meant two different things.** On the city car, the band that climbs
   from the glasshouse shoulder to the roof edge is the roof panel over the flat middle and
   the windscreen and backlight at the ends. Claimed for glass everywhere, the whole roof
   went dark; painted everywhere, the car had no windscreen and no rear window and read as a
   van. It is decided per station, not once.
2. **Wheels sunk inside the body.** Half-track 700 mm against a flank at 831 put all four
   under the arches. Tucked-in wheels are the clearest tell of a body drawn without them.
3. **Bumpers standing proud of the corners** like a shelf, because their half-width was taken
   from the widest station rather than from the station they sit at.
4. **A tail too round**, from stations that tapered where the reference cuts off vertically.

# Pitfalls
- **Do not convert the mesh to get a CAD file.** A mesh converted to STEP is a STEP file full
  of triangles: no face to select, no fillet to edit. Rebuild the same design as solids from
  the same numbers, and keep those numbers in one module both builders read -- two copies
  drift apart on the first change, invisibly, because both files still produce a table. Voir
  run_013.
- **Watch which way the subject faces.** `views.py` puts the `front` camera at -X. A generator
  written nose-first along +X renders its tail in the view labelled front.
- **A screenshot of a CAD model is still only an image.** Those references were shaded
  SolidWorks captures with every face coloured, and they carry exactly as much dimensional
  information as a photograph: none.

# Verification
- The plan lists every image with its fingerprint, and `unrecognised_references` is empty.
- The generator's report names the plan as its input and the reading as its parent.
- `bbox_mm` matches the declared dimensions, and the subject sits on z = 0.
- The reference and the renders are both in the preview, side by side, and someone has
  actually looked at them.

## run_013_choose_the_exchange_format_before_importing_a_cad_model - Choose the exchange format before importing a CAD model
> Status: Active
> Category: other
> Verified: 2026-08-24 (same vehicle, two formats: STL imported 1 object at 100x scale, OBJ from the .blend imported 568 named objects in true millimetres); same day, the return trip: a 132 MB CATIA STEP of 1398 solids arrived as one object at 1000x scale, and a part designed against it went back out as a true B-rep by being rebuilt rather than converted
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.
> Indicators reviewed: 2026-08-24 18:18:19

# Trigger
- A CAD model arrives in more than one form -- a `.blend`, a STEP, and an STL somebody already exported -- and the fastest-looking one is about to be imported.
- Any chain whose later steps sort, name, or delete *parts*: envelope selection, symmetry audit, part transfer, interior removal.

# Prerequisites
- Every available form of the same model, listed before choosing one.
- What the downstream chain needs, written down first. That is the only thing that decides the format.

# Why the convenient file is often the wrong one
An exchange format is a filter. The question is never "can this be imported" -- all of them can -- but **what does it destroy on the way through**. The same vehicle, imported from two files in the same session:

| | STL | OBJ exported from the `.blend` |
|---|---|---|
| objects | **1** | **568**, names kept |
| vertices | 261,134 | 2,191,287 |
| bbox | 279,279 x 168,213 x 155,462 (no unit declared) | 2,778 x 1,678 x 1,540 mm |

The STL is not a smaller version of the same thing. It is a different thing: one welded triangle soup that never had parts. Everything the chain wanted to do next was decided by that.

# Procedure
1. **Name the downstream need before opening anything.** Sorting or deleting parts needs objects. Measuring needs units. Anything else may not care.
2. **Prefer the authoring file** (`.blend`, or STEP through `import_step`) over any mesh somebody exported from it. The export happened for someone else's purpose.
3. **When the authoring file is not directly importable, convert it yourself and pick the format by what must survive.** `import_mesh` reads OBJ, STL and PLY: **OBJ keeps objects separate and named, STL welds everything into one**. One Blender line, not a new operation:
   `bpy.ops.wm.obj_export(filepath=..., export_selected_objects=False, export_materials=False)`
4. **Import, then read the object count against what the source claims.** 568 against 571 is three empties or name collisions and is fine. 1 against 571 means the parts are gone and no later step will bring them back.
5. **Check the bounding box against the real object in millimetres.** STL declares no unit, so a hundredfold error arrives silently and looks like a large model rather than a wrong one. A vehicle is about 2.8 m, not 279 m.
6. **Only now scale.** `recenter --set scale=` once, on the true dimensions, rather than compensating for an unknown unit later in the chain.

# The return trip: getting a solid back out
The same filter runs backwards, and it is worse in that direction. Blender writes no STEP,
because STEP is a B-rep -- planes, cylinders, exact edges -- and Blender holds only meshes.
Converting a mesh to STEP through FreeCAD's *Shape from mesh* does produce a `.stp`, and every
cylinder in it is gone: a 52 mm boss becomes 32 planar facets with no diameter to dimension and
no hole a CAM package can recognise.

**If the part was built from numbers, rebuild it from those numbers.** A bracket composed of
lofts, cylinders and booleans replays in FreeCAD's `Part` module in a few dozen lines and exports
a genuine B-rep: 58 faces of which 10 are `CYLINDRICAL_SURFACE`, 106 KB, volume within 0.15% of
the mesh version -- which is exactly the difference between an exact cylinder and its 32-facet
approximation. This only works because nothing was sculpted; a sculpted surface has no numbers
to replay, and there the tessellated STEP is the honest answer.

Two mechanics worth not rediscovering. `FreeCAD -c script.py` runs the script and then **sits on
its interactive prompt**, which reads as a hang; the headless binary is
`Contents/Resources/bin/freecadcmd`, and it exits on its own -- 0.8 s against a ten-minute
timeout. And `removeSplitter()` after the fusions is not cosmetic: without it every boolean
leaves its seam edges behind and the exported file carries several times the faces, which is
what makes a STEP tedious to dimension.

# What meshanvil does not do
`import_step` exists, `export_step` does not: the tool takes CAD in and only lets mesh out.
`import_step` also writes STL and nothing else, so a 1398-solid STEP arrives as one welded object
-- the loss is imposed by the operation, not chosen by the operator -- and its report carries a
+/-1e100 bounding box, a sentinel rather than a measurement. Read the extent from the import that
follows it, never from the STEP report itself.

# Verification
- Object count from the import report's `findings[0].objects`, compared against the source. This is the check that distinguishes the two files above, and it is one number.
- `bbox_mm` against a dimension you know about the real object. A vehicle, a room, a bracket -- something with an expected size in millimetres.
- After `ray_visibility`, `seen + never_seen` must be the object count. On a one-object import it is 1 + 0, which is the tool telling you it has nothing to sort.
- Warnings from `import_mesh`: `units_not_declared_by_source` is the STL case, and it is exactly the situation where step 5 is not optional.

# Rollback
- Nothing here is destructive: the wrong choice costs the chain built on top of it, not the source. Re-import from the better file and re-run; the reports of the abandoned chain stay as evidence of why.

# Limits to state, not to hide
- OBJ keeps objects and names but not modifiers, parenting or transforms as such -- it bakes them. Verified on this model that no object carried a modifier; a rigged or modifier-driven assembly needs `apply_modifiers` first, and run_006's warning about parent empties applies before any export.
- The object counts here are Blender's OBJ importer against Blender's own exporter. A third-party OBJ may group differently.
- PLY was not exercised in this comparison.

# References
- What becomes possible once parts survive: `run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility`
- What the chain does with those parts afterwards: `run_006_turn_a_cad_assembly_into_a_printable_solid`
- The measurement discipline this relies on: `run_010_verify_that_a_command_did_what_it_appeared_to_do`

## Report facts
- `006` `import_mesh` (ok): params `{"source_format": ".obj", "source_name": "p3d.obj"}`; measurements `{"bbox_mm": {"max": [2320.204, 839.137, 1319.142], "min": [-458.607, -839.073, -221.368]}, "faces": 4302975, "non_manifold_edges": null, "objects": 568, "shells": null, "vertices": 2191287, "volume_cm3": null}`
- `007` `ray_visibility` (ok): params `{"directions": 42, "grid": 110, "rays": 508200}`; measurements `{"bbox_mm": {"max": [2320.204, 839.137, 1319.142], "min": [-458.607, -839.073, -221.368]}, "faces": 4302975, "non_manifold_edges": null, "objects": 568, "shells": null, "vertices": 2191287, "volume_cm3": null}`
- `007c` `drop_unseen` (ok): params `{"cache": ".../p3d_imported_visibility.json", "dropped": 277, "faint_max": 2, "kept": 291, "render": true}`; measurements `{"bbox_mm": {"max": [2320.204, 839.137, 1319.142], "min": [-458.607, -839.073, -221.368]}, "faces": 3884723, "non_manifold_edges": null, "objects": 291, "shells": null, "vertices": 1955779, "volume_cm3": null}`
- The same vehicle through `001` `import_mesh` from `derived-mesh.stl`: `{"objects": 1, "vertices": 261134, "faces": 522732}`, warning `units_not_declared_by_source`, bbox `min [-46604.015, -84102.097, -22889.778]` / `max [232675.064, 84110.771, 132572.174]`.

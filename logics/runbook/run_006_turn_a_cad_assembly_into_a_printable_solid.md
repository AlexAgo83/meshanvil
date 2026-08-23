## run_006_turn_a_cad_assembly_into_a_printable_solid - Turn a CAD assembly into a printable solid
> Status: Active
> Category: other
> Verified: 2026-08-21 (571-mesh assembly to a watertight 1/10 solid, 0 non-manifold edges); 2026-08-24 re-run end to end on the same assembly at 1/13.9 (202 x 123 x 113 mm, 1 shell, 0 non-manifold edges, 413 cm3), which is where the clamp and skip_closed traps below were found
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.
> Indicators reviewed: 2026-08-21 23:13:16

# Trigger
- A printable model is wanted from a CAD assembly: scale model, mock-up, physical prop.

# Prerequisites
- The source file saved, and the whole pipeline run **headless on a copy**. It is destructive by design (it deletes most of the scene) and a voxel remesh over millions of faces will freeze an interactive session for minutes.
- The envelope part list, from run_005, and the parts it rejected already deleted (`drop_unseen`) rather than merely listed.
- **The assembly, not an STL of it.** An STL welds every part into one object, which makes the envelope selection above impossible and leaves the interior permanently inside the result. See run_013.
- The target scale decided first: it sets every other parameter.

# Why a CAD assembly is not printable as-is
Three gaps, none of which a slicer will fix:
- parts are zero-thickness open surfaces; a printer needs closed volumes;
- hundreds of parts interpenetrate; a print needs one solid, not a pile;
- most of the content is never visible from outside and only costs file size.

# Procedure
Parameters below are for 1/10 on a 0.4 mm nozzle; scale them, do not copy them blindly.
1. **Freeze transforms before deleting anything.** For every part you keep, save `matrix_world`, set `parent = None`, restore `matrix_world`. Deleting an empty that parents a kept object teleports that object to its local position, and CAD assemblies parent everything to nested empties. This cost three full pipeline runs: the main body silently shifted about 600 mm sideways while the appendages, parented elsewhere, stayed put. Nothing flagged it; the model was simply wrong.
2. **Delete everything outside the envelope list.**
3. **Join** the survivors into one object.
4. **Solidify**, thickness = minimum printable wall x scale factor (1.2 mm printed -> 12 mm real at 1/10), offset 0. This is what turns surfaces into volumes.
   - **Turn the thickness clamp off.** Blender's Solidify clamps thickness against local geometry to avoid self-intersection, and on tessellated CAD that clamp bites nearly everywhere: the requested wall is silently reduced, the following remesh has less than a voxel to work with, and the result comes out **pitted all over** -- not obviously wrong, just eaten. `thickness_clamp=0` on the same input produced a clean surface at the same thickness. This one parameter decided the outcome twice in one session.
   - **A closed mesh is skipped by default.** Tessellated CAD panels are often already manifold volumes, so `skip_closed=true` (the default) walls nothing at all and reports success. If the report says `walled 0 / already_closed N`, the operation did nothing: pass `skip_closed=false` to thicken a closed body deliberately.
5. **Clean before thickening.** Merge doubles, dissolve degenerate edges, triangulate. Solidify on tessellated CAD reacts to near-zero-area faces by throwing out spikes: one such spike put a vertex 450 mm outside the object's flank and inflated the reported width by 400 mm. Nothing downstream detects this except a bounding box that stops making sense.
6. **Voxel remesh**, voxel = target surface detail x scale factor (0.8 mm printed -> 8 mm real). This single step fixes watertightness, interpenetration and non-manifold geometry at once. Its brutality is the point.
   - Cost is cubic: halving the voxel multiplies memory by eight. At 8 mm over a 2.8 m object it is about 16 M voxels and runs in minutes; at 4 mm it is 130 M and will not finish comfortably.
   - Styling grooves narrower than the voxel are erased. Check the ones that matter before committing to a voxel size.
   - **A coarser voxel does not close openings, it erodes panels.** The intuition that a bigger voxel will bridge a window aperture or a panel gap is wrong: sheet metal thinner than the voxel disappears first. On a body whose walls measured 0.68 mm at print scale, a 2.5 mm voxel turned the bonnet into lace while the apertures stayed open. Thickness comes from step 4; the voxel only ever removes.
   - **The floor is two voxels, and the operation reports it.** `thin_feature` gives `thinnest_mm`, `median_mm` and `share_below_floor`. A `share_below_floor` near 1.0 means the voxel size is not viable for this geometry no matter how the render looks at thumbnail size.
7. **Prune shells by size, never by rank.** Keep every connected component above a vertex threshold; drop only specks.
8. **Measure, scale, export** STL or 3MF in millimetres.

# Verification
- **Compare the output bounding box against the source envelope's.** They must differ only by the wall thickness added, a few millimetres. This single check catches displacement, missing parts and spikes, and it caught every failure in practice while the manifold checks passed throughout.
- Non-manifold edge count must be exactly 0. Count edges whose `link_faces` is not 2.
- Signed volume must be positive and plausible; it also gives the material estimate.
- Bounding box in millimetres against the print bed, including whether the longest dimension fits.
- **Render the result from at least top, front and side, and look at it.** The numeric checks pass on a model with missing parts.

- **Deleting parent empties displaced most of the model.** The result stayed watertight, single-shelled and plausible in a close-up render; only the overall bounding box, compared against the source assembly, showed the 600 mm shift. Same root cause as the offset trap in run_004: a transform that lives in a parent nobody kept.
- **A bad hypothesis cost a run.** The width anomaly was blamed on solidify spikes from degenerate faces, and a cleaning step was added that changed nothing. Locating the offending vertices first would have pointed straight at the parenting. Measure where the anomaly is before deciding what causes it.
- **A solidify spike inflated the bounding box.** See step 4. Caught because the width did not match the known source width, not by any manifold check. Compare the result's bounding box against the source assembly's: they should differ only by the wall thickness you added.

# Mistakes made on the first runs, none caught by the manifold check
- **Keeping only the largest shell deleted every detached appendage.** Anything that does not touch the main skin becomes its own shell after remeshing, and that usually includes the parts you most want to keep. The numeric checks all passed: 0 non-manifold, positive volume, one clean solid. Only the top-down render showed the empty recesses. Prune by size, not by rank.
- **`bound_box` read straight after a bmesh edit is stale.** It reported 230 mm where the true width was 138 mm. After modifying mesh data through bmesh, measure from the vertices, or force a depsgraph update first.

# Rollback
- The pipeline never writes to the source file; it reads it and writes new outputs. Delete the outputs.

# Decisions to put to the operator before running
- Fragile appendages on thin stalks: print separately and glue, or delete. At 1/10 such a stalk is about 3 mm and will break.
- Glazing: filled solid (simple, strong) or hollowed out for clear inserts (needs the glazing separated first).
- Detached appendages: fused to the body or kept as separate bodies.
- Splitting: a 279 mm model does not fit a 256 mm bed. Cut with locating pins, or drop to 1/12.

# Measured afterwards
- A voxel that erases detail is not caught by comparing the voxel to the smallest part. On the
  generated fixture the smallest object extent is 64 mm, so a 30 mm voxel passes that test while
  destroying the trims: a thin feature can sit inside an object whose own bounding box is large.
  What caught it was the bounding-box drift -- 106.5 mm against a 30 mm voxel, where a clean run
  drifts by less than one voxel.
- The same check caught an unrepaired defect leaking through the remesh: 8.8 mm of drift at a
  6 mm voxel with a smeared island still in the file, against 0.6 mm once repaired. Refusing a
  result whose bounding box moved by more than one voxel turns both into an exit code.

# References
- Input: run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility
- Execution channel: run_001_drive_a_live_blender_session_from_the_agent
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)

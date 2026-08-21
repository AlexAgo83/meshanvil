## run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility - Select the outer envelope of an assembly by ray visibility
> Status: Active
> Category: other
> Verified: 2026-08-21 (571 meshes sorted into 73 envelope parts with 508,200 rays, ~2 min headless)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- Only the parts visible from outside are needed: printable model, render-only asset, lightweight viewer export, exploded view of the skin.
- The assembly has hundreds of parts and no reliable grouping to select from.

# Prerequisites
- The source file saved and worked on headless; the sort is read-only but the pipeline that follows is not.
- Do not try to select by name. In CAD-derived scenes naming is inconsistent across suppliers and revisions, and it silently omits parts. Visibility is measurable; naming is a convention.

# Procedure
1. Compute the assembly's global bounding box and centre from every mesh's world-space `bound_box`.
2. Generate N directions with a Fibonacci sphere (42 is enough for an object a few metres across; the count controls angular coverage, not accuracy per view).
3. For each direction, cast a GRID x GRID array of *parallel* rays from outside the bounding sphere inwards. Parallel rays over a grid, not one ray per direction: a single ray samples one silhouette point and tells you almost nothing.
4. Record per hit object: total hits, hits from above (`d.z > 0.35`), hits from below (`d.z < -0.35`). The hemisphere split is what makes the result actionable.
5. Classify with two thresholds rather than one:
   - hits outside the lower hemisphere >= 20 -> the envelope;
   - hits >= 20 but nearly all from below -> underbody, drop it for a printable model since the underside gets closed anyway;
   - 1 to 4 hits -> glimpsed through a panel gap, negligible;
   - 0 hits -> internal, never seen.
6. Write the classification to JSON and review the envelope list by eye before consuming it. It should read like a parts list a human would write.

# Verification
- The envelope list contains every panel you can name from a walkaround, and nothing you cannot see.
- Counts add up to the total mesh count.
- Sanity check the extremes: the most-hit object should be the largest exterior surface, and known-internal parts should be absent.

# Rollback
- Read-only. Nothing to undo.

# Observed numbers (one assembly, for calibration)
- 571 meshes, 42 directions x 110x110 rays = 508,200 rays, about two minutes headless.
- 375 seen at least once, 196 never seen.
- Thresholded: 73 envelope, 75 underbody-only, 132 glimpsed, 196 internal.
- Internal parts seen through openings in the outer skin land in the envelope set. That is correct behaviour, not a bug: they are visible. Decide downstream whether to keep them.

# References
- Execution channel: run_001_drive_a_live_blender_session_from_the_agent
- Consumed by: run_006_turn_a_cad_assembly_into_a_printable_solid
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)

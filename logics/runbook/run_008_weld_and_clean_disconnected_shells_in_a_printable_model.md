## run_008_weld_and_clean_disconnected_shells_in_a_printable_model - Weld and clean disconnected shells in a printable model
> Status: Active
> Category: other
> Verified: 2026-08-21 (two loose appendages welded to a body, 3 shells reduced to 1, 0 non-manifold edges)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- A printable model comes out in several disconnected pieces that should print as one: a round part sitting in a recess, a part on a thin stalk, anything separated by a real-world clearance gap.
- Small fragments float free after a boolean cut.

# Why it happens
A voxel remesh cannot bridge a gap wider than its voxel. Real clearances survive as real gaps, so exactly the parts you most want attached come out loose. Raising the voxel size to bridge them destroys surface detail everywhere else; use a local weld instead.

# Procedure: welding with a pin
1. **Enumerate the shells** by flood-filling the vertex graph. Print each shell's vertex count and world bounding box. Sizes alone are ambiguous; the bounding boxes identify what each shell is.
2. **Probe for material before placing anything.** March a ray across the gap and print every hit position. Both parts are usually hollow shells, so a pin aimed at the obvious centre passes clean through both without touching either.
   - Observed here: a pin on the appendage's axis, aimed inboard, hit nothing. The ray showed hits only at the appendage's own walls and then at the far side of the object: at that height, the recess has no material behind the appendage.
   - The same probe fired upward found the appendage's top at 65.1 mm and the recess wall at 73.4-74.9 mm, an 8.3 mm gap. That is where the pin belongs.
3. **Place the pin so it crosses both walls**, extending a few millimetres past each. Size it for the load, not for discretion: it is what holds the part on.
4. **Boolean UNION, solver EXACT**, one pin at a time.
5. **Re-enumerate the shells after each union.** The count must drop by one each time. If it does not, the pin missed: go back to step 2 rather than resizing blindly.

# Procedure: cleaning debris
Every boolean DIFFERENCE detaches fragments that were only attached through the removed region. Enumerate shells and delete every one below a size threshold, then re-check. Observed: 5 fragments after cutting a floor hatch, 2 more after removing a 20 mm rod. Run the cleanup as a standing step after any cut, not as a reaction to seeing something float.

# Verification
- Shell count is 1 (or the intended number).
- Free edges stay 0 through every operation.
- Bounding box unchanged.
- Render the welded area from outside and confirm the pin is hidden by the surrounding skin.

# Using asymmetry to classify leftovers
A feature present on one appendage and absent on its three counterparts is almost certainly import debris, not design intent. Before removing anything the operator points at, test the three mirrored positions. It costs one query and turns a judgement call into evidence. See [[run_002_audit_symmetry_of_an_imported_cad_assembly]] for the same test used in the opposite direction, to find what is missing.

# Rollback
- Work on a copy, or keep the pre-weld file; unions and cuts are not reversible in place.

# References
- Input: run_006_turn_a_cad_assembly_into_a_printable_solid, run_007_hollow_a_printable_body_for_electronics
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)

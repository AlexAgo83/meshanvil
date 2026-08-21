## run_004_transfer_parts_between_two_cad_derived_blend_files - Transfer parts between two CAD-derived blend files
> Status: Active
> Category: other
> Verified: 2026-08-21 (30 parts of one thin appendage moved between two exports of the same assembly, final placement error 0.4 mm)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- A part missing from the working model exists in another blend file (an older export, a supplier delivery, a variant).
- The operator asks whether the part can be brought across.

# Prerequisites
- Read access to the donor file. Never open it in the operator's live session: inspect it headless (`Blender -b donor.blend -P inspect.py`) so a broken donor cannot damage the working scene.
- The working scene is saved before anything is appended.

# Procedure
1. **Inspect the donor headless.** Print unit settings, object count, global bounding box, and the names matching the target part. Do not append yet.
2. **Compare unit scale.** Both must resolve to the same real-world scale. A donor authored in millimetres lands 1000x oversized; catch it here, not visually.
3. **Look for a shared frame before computing any alignment.** List objects whose names exist in *both* files and compare their world bounding-box centres. Identical centres on two or three independent parts (spread across the model, not clustered) mean the files share an origin and no alignment is needed at all. This is the common case for two exports of the same CAD assembly, and it turns a hard problem into a copy.
   - Only if the centres differ: pick three or more non-collinear correspondences and solve the rigid transform.
   - Local `dimensions` may come out axis-permuted between the files even when world centres match. That is a per-object rotation difference, not a misalignment: trust the world centre.
4. **Record the expected world centre of two donor parts before appending.** This is the only way step 6 can catch a silent offset.
5. **Append by name filter** with `bpy.data.libraries.load(path, link=False)`, selecting only the parts wanted, and link them into a dedicated collection so the import stays reversible as a unit.
6. **Verify placement against step 4, and expect it to fail.** Appended objects keep a `parent` pointer to an object that was not part of the filter; the parent transform is then missing and everything lands offset. Observed here: a uniform 101 mm error, small enough to look plausible in a viewport.
   - Fix: dump each donor object's `matrix_world` headless to JSON, then in the target set `ob.parent = None` and `ob.matrix_world = Matrix(dumped)`.
   - Alternatively include the parent chain in the name filter, but the explicit matrix is more predictable.
7. Re-verify the reference centres. Residual should be at the rounding precision of the recorded references.

# Verification
- Reference centres match to sub-millimetre.
- The imported bounding box is laterally symmetric when both sides were imported.
- Render the region and look at it. Numeric agreement plus a plausible render is the acceptance bar.

# Rollback
- Delete the dedicated collection and its objects; nothing else in the scene was touched.

# Limits to state
- Materials come across from the donor and will not match the target's look.
- Donor mesh quality is inherited. An export-derived donor carries its own defects (in the case handled here, a known glitch on one front lamp); name-filtering the import keeps those defects out only if they live in parts you did not select.
- Vertex counts differing between same-named parts across the two files is normal (different tessellation) and is not evidence of misalignment.

# References
- Execution channel: run_001_drive_a_live_blender_session_from_the_agent
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)

## run_002_audit_symmetry_of_an_imported_cad_assembly - Audit symmetry of an imported CAD assembly
> Status: Active
> Category: other
> Verified: 2026-08-21 (found a genuinely missing part in a ~700-object assembly)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- Looking for a missing, forgotten or duplicated part in an imported assembly (STEP/CATIA into Blender).
- The operator suspects something is missing and asks for confirmation. A suspicion is not a finding: this procedure exists to put numbers on it.

# Prerequisites
- Access to the scene, via run_001 or headless.
- Know the symmetry plane. Do not assume it: derive it from existing pairs (pairs matching within 2 mm confirm a clean plane) and from the product's longitudinal axis.

# Procedure
1. **Target inventory.** Filter object names by domain keywords (case-insensitive regex, covering both source-language and English variants). Print type, dimensions and world centre.
2. **Object-level symmetry test.** For each off-axis part, look for a counterpart at the mirrored centre. A part named `_L` with no `_R` is a hint, not proof: geometry decides, not naming.
3. **Intra-object symmetry test.** A single object may bundle several sub-elements. Split the mesh into connected islands (union-find over edges), compute each island's centre, then pair them up. An island with no counterpart is the finding.
4. **Corroboration.** Before concluding, list every part whose centre lies within ~300 mm of the suspect location. Interface parts present (seal, bracket, fixing) without the main component is the strongest confirmation: the surrounding trim was modelled, the component itself never imported.
5. **Visual check.** Isolate the part family (hide everything else), orthographic top or front view, viewport render. This is the step that separates a true absence from a hidden or mis-named part. Restore visibility afterwards.
6. **Repair, only when the absence is an asymmetry.** Rebuild by mirroring: transform vertices to world space, negate the lateral coordinate, reverse polygon loop order so normals stay outward, carry over materials, per-face material index, collection and parent from the source. Create a new object; never modify the source part.

# Verification
- The rebuilt object must have exactly the source's vertex and face counts, identical dimensions, and an exactly mirrored centre.
- Its distance to the interface parts on the repaired side must match the source's distance to its own interfaces.
- Render both sides together, never one alone: a presumed mirror is not a verified mirror.

# Rollback
- Delete the created object; the source was never touched. `Ctrl+Z` on the operator's side.

# Limits to state, not to hide
- The mirror is purely geometric. A production part that is genuinely asymmetric (cut-out, keying feature, cable routing) will come out wrong.
- An absence on **both** sides is not an asymmetry and this procedure cannot repair it: an import is missing, not a part. Say so instead of fabricating one.
- A placeholder volume eyeballed into place to "look right" is not a part: it holds for an image, not for an integration review. Name it explicitly (`*_dummy_*`), check its bounding-box overlaps against neighbouring parts, and report it as provisional.
- Iterative visual placement through the bridge costs ~0.5 s per attempt and converges poorly. After two failed attempts, hand control back: select the object and let the operator drag it, which is an order of magnitude faster.

# References
- Execution channel: run_001_drive_a_live_blender_session_from_the_agent
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)

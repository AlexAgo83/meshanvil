## run_009_repair_export_defects_in_a_cad_derived_mesh - Repair export defects in a CAD-derived mesh file
> Status: Active
> Category: other
> Verified: 2026-08-21 (one smeared patch repaired and 186 coincident duplicates removed in a 2109-object donor, 5.59 M vertices)
> Related request: (none yet)
> Related backlog: (none yet)
> Related task: (none yet)
> Reminder: Update status, category, verification, and linked refs when you edit this doc.

# Trigger
- A tessellated export (CATIA/STEP to Blender) carries a known or suspected glitch: a part that renders as a spike, a streak, a shard reaching across the whole assembly.
- Before reusing a donor file as a source. A defect found by eye is one defect; the same export usually carries a class of them, and the file is worth sweeping once rather than being surprised later.

# Prerequisites
- Work headless on a copy under `work/out/`. Never write to `work/in/`, never save the operator's session.
- Know the mirror plane and which sign of the lateral axis is which side. Derive it from a part that is unambiguously left or right; do not assume.

# Procedure
1. **Locate by bounding box, not by eye.** Group objects by name family and print each family's world bounding box. A defective part announces itself as a box orders of magnitude larger than its twin: 1.8 x 3.2 x 0.65 m against 0.43 x 0.28 x 0.26 m for the same trim on the other side. This is one script and it beats any amount of orbiting the viewport.
2. **Isolate the defect down to the connected component.** Split the object into islands (union-find over edges) and print per-island bounding boxes. A tessellation smear is almost always local: 45 vertices out of 5383, one island out of 869. Repairing the island preserves the 868 healthy ones.
3. **Separate the dragged vertices from the intact ones.** Within the bad island, classify vertices as in-zone or outlier against the part's expected volume. Outliers strung along a straight line are the signature: the export dragged a patch along a direction instead of closing it.
4. **Find the mirror twin of the island, not of the object.** Mirror the in-zone vertices across the symmetry plane and score every island of the counterpart object by how many vertices coincide. The best score is the twin; a clear winner (22/24 against 3/24 for the runner-up) confirms it. Ambiguity here means stopping, not guessing.
5. **Graft, do not rebuild the whole side.** Delete the bad island's faces and vertices, then recreate the twin's faces with the lateral coordinate negated and the winding reversed so normals stay outward. Weld coincident vertices as you create them. Whole-side mirroring is the tempting shortcut and it is wrong: the two sides of a CAD export are rarely tessellated identically (~110 islands of 869 differed here), so it would replace healthy data to fix 45 vertices.
6. **Sweep the file for the same class of defect.** For every object, compare the full bounding box against a robust one built from the 5th-95th percentile of each coordinate. A smear inflates the first and leaves the second untouched; a ratio above ~2.5 flags it. Expect legitimate hits: a thin rod, a linkage arm, anything genuinely elongated. Read each flag before acting on it.
7. **Sweep for coincident duplicates.** Bucket objects by (vertex count, face count, world bounding box), then confirm each bucket with a hash of the world-space coordinates. Only byte-identical, same-place copies are redundant. Keep one per group and delete the rest. Repetition at a different position is not a duplicate: four identical parts mounted in four places are four parts.

# Verification
- Compare the repaired object's bounding box against its mirror twin. Here: X -317.1..115.7 / Y 376.0..655.1 / Z 520.8..775.7 against a twin at X -317.0..116.0 / Y -655.0..-376.0 / Z 521.0..776.0.
- Compare the whole file's bounding box against the source, computed by the same script on both. The only coordinates that may move are the ones the defect was inflating. Here X min and both Y bounds moved; Z and X max did not, and Y came back symmetric to 0.1 mm.
- Island count must be unchanged by a graft: 869 before, 869 after. Vertex and face counts drop slightly (welding), they must not rise.
- Compare the non-manifold edge ratio between the repaired part and its twin. In a tessellated CAD export both sit around 60% because every surface patch is an open shell. Equality between sides is the signal; a low absolute number is not, and chasing it here means misreading the format.
- Render both sides in the same frame, front view. A part rendered alone always looks plausible.

# Rollback
- Delete the file under `work/out/`. The source in `work/in/` was never opened for writing.

# Limits to state, not to hide
- The graft assumes the part is mirror-symmetric. A genuinely asymmetric feature on the repaired side (cut-out, cable routing, keying) will come out wrong; check the twin against the drawing before trusting it.
- The percentile sweep only catches defects that move vertices far away. A patch collapsed in place, an inverted normal, a hole of the right size are invisible to it.
- Do not audit left/right completeness by comparing vertex counts. The two sides are not tessellated identically, so the test returns hundreds of false positives (1387 out of 1923 objects here) and buries any real finding. Use a per-part Hausdorff distance, or do not claim to have checked.
- Name-based classification does not establish whether a part is useful. 38.7% of the vertices fell outside every keyword here, and most of them were outer skin. Ray visibility decides that question (run_005), naming does not.
- Save compressed. A `compress=False` save took a 194 MB file to 490 MB for nothing.

# References
- Symmetry audit at object level: run_002_audit_symmetry_of_an_imported_cad_assembly
- Useful-part selection: run_005_select_the_outer_envelope_of_an_assembly_by_ray_visibility
- Cross-file part transfer: run_004_transfer_parts_between_two_cad_derived_blend_files
- Related request: (none yet)
- Related backlog: (none yet)
- Related task: (none yet)

## req_004_demonstrate_on_a_clean_organic_subject_what_the_vehicle_chain_cannot_show - Demonstrate on a clean organic subject what the vehicle chain cannot show
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 18:01:34

# AI Context
- Summary: The demonstration has one subject and every report in it is a defect being found, at a scale where an absolute voxel and a relative one feel identical. A sound organic subject reduced to a 180 mm figurine shows sweeps staying silent, and shows two voxel sizes both passing every check while only one keeps the fingers.
- Keywords: demonstration, clean subject, negative control, voxel fraction, print size, second project, figurine
- Use when: adding or changing a demonstration subject, or explaining what a passing check does and does not measure.
- Skip when: the change concerns an operation's behaviour rather than what the demonstration shows.
# Needs
- The demonstration has one subject, a vehicle modelled for rendering, and every report in it is a defect being found; nothing shows the sweeps staying silent when a model is sound.
- The vehicle is remeshed at its real size, where a voxel in millimetres and a voxel as a fraction of the subject feel like the same number, so the chain never shows that voxel size is meaningless without the subject's size.
- Measured on a human base mesh reduced to a 180 mm figurine: a 1.5 mm voxel and a 0.5 mm voxel both report ok, one shell, no non-manifold edge, and at most 1.3% of volume lost, while the renders show fingers fused into mittens at 1.5 mm and separated at 0.5 mm.
- The vehicle carries parts sealed inside its body, so visibility always finds something; a subject with nothing hidden would show what a clean visibility result reads like.
- A second subject cannot share the current work directory: its reports would take the vehicle's identity numbering and merge into an outliner group named after the vehicle.

# Context
- The subject is a sculpting base mesh: one object, pure quads, closed or nearly closed, no modifier, no material -- the opposite of the vehicle in every property the chain reads.
- The vehicle chain's repair steps are no-ops on it, and walling it is actively wrong: it hollows a solid body rather than giving an open panel a thickness.
- The only import operation is `import_step`, which needs FreeCAD; a subject delivered as OBJ alone cannot enter the pipeline today.
- This request depends on multi-project workspaces: without them two demonstration chains share one identity counter, one outliner group and one retention window.
- The existing demonstration asset and its provenance record set the pattern for shipping a second one.

# Acceptance criteria
- AC1: A second demonstration subject ships as a project of its own, with its own provenance record, and does not disturb the vehicle demonstration in any way.
- AC2: The chain shows a sound subject passing: the defect sweep reports no finding and the report reads as a deliberate result rather than an absence of data.
- AC3: The chain sets the subject's size explicitly as a decision, taking it from its authored size to a print size, and the reports state both.
- AC4: A branch remeshes the same subject at two voxel sizes chosen as fractions of the subject, both reporting ok on every topology and volume check, so the difference is visible only in the renders.
- AC5: The documentation states the lesson the branch carries: a voxel size is a fraction of the subject, and the checks that pass do not measure feature loss.
- AC6: A visibility pass on a subject with nothing sealed inside reports that explicitly rather than silently.
- AC7: Both demonstration projects rebuild from a single command each, and the checks that guard the first also guard the second.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_005_demonstrations_that_show_the_checks_discriminating`
- Architecture decision(s): (none yet)

# References
- tools/build_demo_chain.sh
- tools/strip_asset.py
- tools/voxel_remesh.py
- tools/recenter.py
- tools/scan_defects.py
- README.md

# Backlog
- `item_026_ship_the_figurine_subject_as_its_own_demonstration_project`
- `item_027_build_the_figurine_chain_around_a_sound_subject_and_a_size_decision`
- `item_028_branch_the_remesh_at_two_fractions_of_the_subject`

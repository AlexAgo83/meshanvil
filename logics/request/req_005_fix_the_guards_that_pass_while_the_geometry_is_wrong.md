## req_005_fix_the_guards_that_pass_while_the_geometry_is_wrong - Fix the guards that pass while the geometry is wrong
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 14:31:41

# AI Context
- Summary: Three guards report a number that answers a different question than the one asked, all found by running existing operations on sculpting base meshes: the thin-feature measure reads object bounds, walling decides on a zero test, and a mesh-only source cannot enter the chain at all.
- Keywords: thin feature, smallest object extent, walling tolerance, openness ratio, mesh import, guard correctness
- Use when: changing what an operation measures before it acts, or what it records about a decision it took.
- Skip when: the change is about a viewer surface or a path, with no measurement behind it.
# Needs
- Running the pipeline on sculpting base meshes rather than the vehicle exposed guards that report a result they did not measure.
- `voxel_remesh` records `smallest_input_extent_mm` as the smallest object's bounding extent, so on a single-object organic subject it reported 180 mm for a 180 mm figurine and could not warn that the fingers were about to be erased. The guard is blind on any subject whose thin features are not separate objects.
- `solidify` treats a body as open unless it has exactly zero open edges. A figure with 4 open edges out of 14 803 faces was walled: 14 813 vertices became 29 626 and a solid body became a shell with a wall inside it. A body that is 0.03% open should be repaired or reported, not thickened.
- A subject delivered as OBJ alone cannot enter the pipeline; the only import operation needs FreeCAD and reads STEP.
- The project's own rule is that a geometric claim gets a number, and these three report numbers that do not answer the question being asked.

# Context
- These were found by running the existing operations on assets from a different class, not by reading the code.
- The vehicle never exposed them: its parts are separate objects, its panels are wide open, and it arrives as a .blend.
- `smallest_input_extent_mm` is written into the report parameters, so changing what it measures changes what a reader is told, not only what the operation logs.
- A wall thinner than one voxel is erased by the remesh that follows, which is why the thin-feature measure and the walling decision are related and belong in one request.
- The reports already carry a warning vocabulary, so a guard that cannot decide can say so rather than staying silent.

# Acceptance criteria
- AC1: The remesh states the thinnest feature it is about to remesh, measured on geometry rather than on object bounds, and warns when that feature is at or below the voxel size.
- AC2: The figurine case is covered: a 180 mm single-object subject remeshed at a voxel that erases its fingers produces a warning naming the thin feature, and the same subject at a voxel that keeps them does not.
- AC3: Walling decides on how open a body is rather than on whether it is open at all, and a body that is closed within a stated tolerance is repaired or left alone instead of thickened.
- AC4: A subject that is walled when it should not have been is visible in the report: the operation records what it decided and why.
- AC5: A mesh source that is not a .blend can enter the pipeline through a recorded operation rather than a hand-run script.
- AC6: Each fixed guard has a check that fails when the guard goes back to reporting what it does not measure.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_006_guards_that_measure_what_they_claim`
- Architecture decision(s): (none yet)

# References
- tools/voxel_remesh.py
- tools/solidify.py
- tools/scan_defects.py
- meshanvil_engine/report.py
- scripts/fixture_check.py
- README.md

# Backlog
- `item_029_measure_the_thinnest_feature_not_the_smallest_object`
- `item_030_decide_walling_on_how_open_a_body_is`
- `item_031_let_a_mesh_source_enter_the_pipeline`

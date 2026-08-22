## item_029_measure_the_thinnest_feature_not_the_smallest_object - Measure the thinnest feature, not the smallest object
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 33%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 14:02:34

# AI Context
- Summary: `smallest_input_extent_mm` is the smallest object's bounding extent, so a one-object figurine reported 180 mm while a 1.5 mm voxel erased its fingers. The guard has to measure geometry, warn against the voxel about to be used, and say it is an estimate.
- Keywords: smallest_input_extent_mm, thin feature, object bounds, voxel warning, organic subject
- Use when: changing what the remesh measures before it runs, or what it warns about.
- Skip when: the change concerns the remesh result rather than the check that precedes it.
# Problem
- `smallest_input_extent_mm` is the smallest object's bounding extent, which equals the whole subject when the subject is one object.
- On a 180 mm figurine it reported 180 mm while a 1.5 mm voxel fused the fingers into mittens.
- The report therefore tells a reader the smallest thing at risk is the entire model, which is never true and is worst on organic subjects.

# Scope
- In:
  - Estimate the thinnest feature from the geometry itself rather than from object bounds.
  - Warn when the estimate is at or below the voxel about to be used.
  - Keep the estimate cheap enough to run before every remesh, and say so when it is only an estimate.
- Out:
  - An exact medial-axis or wall-thickness solver.
  - Blocking a remesh the operator asked for; the guard reports, it does not refuse.

# Acceptance criteria
- AC1: The remesh records a thin-feature measure taken from geometry, distinct from the smallest object extent.
- AC2: A voxel at or above that measure produces a warning naming it; a voxel below it does not.
- AC3: The single-object figurine case is asserted, including the voxel that erases the fingers and the one that keeps them.
- AC4: The measure states that it is an estimate wherever it is shown.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: The remesh records a thin-feature measure taken from geometry, distinct from the smallest object extent.
- request-AC2 -> This backlog slice. Proof: AC2: A voxel at or above that measure produces a warning naming it; a voxel below it does not.
- request-AC6 -> This backlog slice. Proof: AC3: The single-object figurine case is asserted, including the voxel that erases the fingers and the one that keeps them.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_006_guards_that_measure_what_they_claim`
- Architecture decision(s): (none yet)
- Request: `req_005_fix_the_guards_that_pass_while_the_geometry_is_wrong`
- Primary task(s): `task_019_fix_the_guards_that_pass_while_the_geometry_is_wrong`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

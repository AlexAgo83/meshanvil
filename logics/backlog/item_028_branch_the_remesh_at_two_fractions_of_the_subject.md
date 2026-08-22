## item_028_branch_the_remesh_at_two_fractions_of_the_subject - Branch the remesh at two fractions of the subject
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Low
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 15:01:05

# AI Context
- Summary: Measured: 1.5 mm and 0.5 mm on a 180 mm figurine both report ok, one shell, no non-manifold edge, at most 1.3% volume lost -- and one fuses the fingers into mittens. The branch keeps both and states that a voxel is a fraction of the subject.
- Keywords: voxel fraction, feature loss, passing checks, sibling branch, documented lesson
- Use when: building or explaining the two-voxel comparison, or writing what the passing checks do not measure.
- Skip when: the change adds a new check; the branch exists to show the current ones passing.
# Problem
- The vehicle is remeshed at its real size, where an absolute voxel and a relative one feel like the same number.
- Measured on the figurine, 1.5 mm and 0.5 mm both pass every check while one destroys the hands and the other does not.
- Nothing in the documentation states that a passing volume and shell count do not measure feature loss.

# Scope
- In:
  - Two sibling remeshes of the same parent, at voxel sizes chosen and stated as fractions of the subject.
  - Keep both results whatever they report, including when both report ok.
  - State the lesson where a reader of the demonstration will meet it.
- Out:
  - Adding a feature-thickness check, which is a separate defect.
  - Tuning voxel sizes until one of them fails for the sake of a red node.

# Acceptance criteria
- AC1: Two sibling remeshes exist on the same parent with their voxel sizes recorded both in millimetres and as a fraction of the subject.
- AC2: The reports show the topology and volume checks passing on both, so the difference appears only in the renders.
- AC3: The documentation states that a voxel is a fraction of the subject and that the passing checks do not measure feature loss.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: Two sibling remeshes exist on the same parent with their voxel sizes recorded both in millimetres and as a fraction of the subject.
- request-AC5 -> This backlog slice. Proof: AC2: The reports show the topology and volume checks passing on both, so the difference appears only in the renders.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_005_demonstrations_that_show_the_checks_discriminating`
- Architecture decision(s): (none yet)
- Request: `req_004_demonstrate_on_a_clean_organic_subject_what_the_vehicle_chain_cannot_show`
- Primary task(s): `task_018_deliver_the_figurine_demonstration_project`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

## item_003_read_the_chain_of_operations_in_a_local_viewer - Read the chain of operations in a local viewer
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Operation review loop
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: A static local page over work/ops/: operations in execution order, and for one of them its measurements, its per-axis bounding-box comparison and its renders side by side.
- Keywords: local viewer, operation timeline, verification renders, static page, no build step
- Use when: Changing how an operator reviews what an operation did.
- Skip when: Anything that runs or edits geometry -- the viewer only reads reports.

# Problem
- Reviewing an operation means reopening Blender and navigating to the affected geometry, which is slow enough that the review is skipped.
- The measurements and the renders exist separately, so the render is read on its own -- exactly the mistake the runbooks warn against.
- There is no view of the chain: which operation ran before this one, and what it changed.

# Scope
- In:
  - A static local page listing the reports in execution order, with status and the axes that moved shown per operation.
  - A detail view for one operation: its measurements, its bounding-box comparison against the input, and its renders next to the numbers they illustrate.
  - Reading report files directly from work/ops/ with no build step and no server requirement.
  - An empty state that explains how to produce the first report.
- Out:
  - Editing, re-running or triggering operations from the viewer.
  - A 3D viewport. The renders an operation produced are what is shown.
  - Integration into the Logics viewer.

# Acceptance criteria
- AC1: Opening the viewer with reports present lists them in execution order with each one's status.
- AC2: Selecting an operation shows its measurements, its per-axis bounding-box comparison and its renders on one page.
- AC3: The viewer opens with no Blender process running, no build step and no network access.
- AC4: With no reports present the viewer states how to produce one instead of failing.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC1: Opening the viewer with reports present lists them in execution order with each one's status.
- request-AC6 -> This backlog slice. Proof: AC2: Selecting an operation shows its measurements, its per-axis bounding-box comparison and its renders on one page.
- request-AC8 -> This backlog slice. Proof: AC3: The viewer opens with no Blender process running, no build step and no network access.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): (none yet)
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Primary task(s): `task_001_deliver_the_reviewable_operation_loop`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.

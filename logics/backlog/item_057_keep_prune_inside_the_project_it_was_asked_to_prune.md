## item_057_keep_prune_inside_the_project_it_was_asked_to_prune - Keep prune inside the project it was asked to prune
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Low
> Theme: Destructive safety
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: A containment condition in prune.candidates so a report pointing outside the active project selects nothing, which also removes the traceback that currently follows the deletion.
- Keywords: prune, inside, project, asked
- Use when: touching what prune is allowed to select or delete.
- Skip when: changing the pinned, linked-document or work/in exclusions, or where an operation may write its output.

# Problem
- prune.candidates accepts any absolute output path a report carries and only excludes paths under work/in, so a report pointing outside the project selects a file outside the project.
- prune.run unlinks before the caller prints, and cli prints with Path.relative_to, which raises on exactly the paths that were not contained -- the deletion happens, then the traceback.
- prune --dry-run raises the same exception, so the dry run cannot warn about the case it exists to warn about.

# Scope
- In:
  - A containment condition in prune.candidates rejecting any output path not inside the active project root.
  - One selfcheck asserting that such a report is not a candidate and that its file survives a prune with keep 0, plus its pytest wrapper.
- Out:
  - Changing the pinned, linked-document or work/in exclusions that already decide what prune may touch.
  - Reporting skipped out-of-project paths to the operator as a new message, unless the check shows one is needed.
  - The report schema, or where an operation is allowed to write its output.

# Acceptance criteria
- AC1: A report whose output path resolves outside the active project is not returned by prune.candidates.
- AC2: prune and prune --dry-run both exit without an unhandled exception on such a report, and the out-of-project file still exists afterwards.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: A report whose output path resolves outside the active project is not returned by prune.candidates.
- request-AC8 -> This backlog slice. Proof: AC2: prune and prune --dry-run both exit without an unhandled exception on such a report, and the out-of-project file still exists afterwards.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_013_a_host_boundary_that_matches_its_own_documentation`
- Architecture decision(s): (none yet)
- Request: `req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented`
- Primary task(s): `task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

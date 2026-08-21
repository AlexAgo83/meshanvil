## item_015_complete_the_mockup_review_controls_without_weakening_the_local_page_boundary - Complete the mockup review controls without weakening the local page boundary
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 40%
> Complexity: Medium
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:26:05

# AI Context
- Summary: Add the mockup's filter, report navigation, labelled native wipe and first-run structure using current local data only.
- Keywords: complete, mockup, review, controls, weakening, local, page, boundary
- Use when: Improving review controls and no-data guidance inside the existing local page.
- Skip when: Adding command menus, workspaces or browser smoke coverage.

# Problem
- Finding a report in a longer chain and moving among report sections still requires manual scrolling.
- The in-place wipe lacks the mockup's explicit state labels and visible affordance.
- The first-run page is informative but omits the reviewed starter and recent-chain structure.

# Scope
- In:
  - A local outliner filter, report-section rail, labelled native comparison control and first-run panels driven by existing doctor and report data.
  - No-report and no-comparison states with explicit guidance.
- Out:
  - Persisting UI preferences or introducing a database.
  - Inventing a command when a manifest does not expose one.

# Acceptance criteria
- AC1: Filtering is reversible and hides only nonmatching visible rows.
- AC2: The comparison divider remains draggable and keyboard-adjustable while before/after labels identify the two states.
- AC3: First run describes a valid next command and every displayed environment state has an explanation.

# AC Traceability
- request-AC3 -> This backlog slice. Proof: AC1: Filtering is reversible and hides only nonmatching visible rows.
- request-AC4 -> This backlog slice. Proof: AC2: The comparison divider remains draggable and keyboard-adjustable while before/after labels identify the two states.
- request-AC5 -> This backlog slice. Proof: AC3: First run describes a valid next command and every displayed environment state has an explanation.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_002_reviewable_local_viewer_interaction_parity`
- Architecture decision(s): (none yet)
- Request: `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`
- Primary task(s): `task_012_deliver_reviewed_viewer_interaction_parity`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_015_complete_the_mockup_review_controls_without_weakening_the_local_page_boundary`

## item_016_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture - Exercise the viewer in a real browser against the generated fixture
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Low
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:26:05

# AI Context
- Summary: Exercise the generated fixture in Chrome and retain only temporary screenshots, not golden images or a new test framework.
- Keywords: exercise, viewer, real, browser, against, generated, fixture
- Use when: Verifying visible browser behavior after a viewer change.
- Skip when: Testing report generation or asserting host-only Python logic.

# Problem
- Host self-checks inspect payloads and source invariants but do not prove browser layout, tab changes, filtering or drag behavior.
- The reviewed mockup and current viewer had never been captured at the same viewport for an explicit parity audit.

# Scope
- In:
  - A small repeatable Chrome smoke script that builds the fixture page, opens it at a fixed viewport, interacts with the defined controls and writes screenshots to a temporary directory.
  - Assertions on observable DOM state and native range values; screenshots are review artefacts, not committed golden images.
- Out:
  - A cross-platform pixel-diff suite or committed screenshots.
  - A new browser-test framework when Chrome and platform tooling already provide the needed smoke path.

# Acceptance criteria
- AC1: One command produces a fixture-page screenshot and fails when Chrome cannot load the page.
- AC2: The smoke test verifies a tab change, a filtered row set and a changed native wipe value.
- AC3: The test leaves no generated browser artefact tracked by Git.

# AC Traceability
- request-AC6 -> This backlog slice. Proof: AC1: One command produces a fixture-page screenshot and fails when Chrome cannot load the page.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_002_reviewable_local_viewer_interaction_parity`
- Architecture decision(s): (none yet)
- Request: `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`
- Primary task(s): `task_012_deliver_reviewed_viewer_interaction_parity`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_013_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture`

# Notes
- Task `task_013_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture` was finished via `logics-manager flow finish task` on 2026-08-22.

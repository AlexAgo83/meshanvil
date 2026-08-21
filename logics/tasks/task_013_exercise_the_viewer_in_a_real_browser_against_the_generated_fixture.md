## task_013_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture - Exercise the viewer in a real browser against the generated fixture
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:30:18

# AI Context
- Summary: Verify the generated fixture in a real browser once workspace, filter and wipe controls exist; screenshots remain temporary evidence.
- Keywords: exercise, viewer, real, browser, against, generated, fixture
- Use when: Adding browser-level coverage for the local viewer.
- Skip when: Implementing controls that the smoke test will exercise.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_016_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture`

# Acceptance criteria
- AC1: One command produces a fixture-page screenshot and fails when Chrome cannot load the page.
- AC2: The smoke test verifies a tab change, a filtered row set and a changed native wipe value.
- AC3: The test leaves no generated browser artefact tracked by Git.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_013_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_013_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture.md` after implementation.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

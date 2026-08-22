## task_013_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture - Exercise the viewer in a real browser against the generated fixture
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 95%
> Confidence: 90%
> Progress: 95%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-22 02:02:01
> Owner: codex

# AI Context
- Summary: Verify the generated fixture in a real browser once workspace, filter and wipe controls exist; screenshots remain temporary evidence.
- Keywords: exercise, viewer, real, browser, against, generated, fixture
- Use when: Adding browser-level coverage for the local viewer.
- Skip when: Implementing controls that the smoke test will exercise.

# Definition of Done (DoD)
- [x] The backlog scope is implemented.
- [x] Acceptance criteria are covered.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

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
- `make check` passed on 2026-08-22 after adding the smoke script and selector regression check.
- `make viewer-smoke` passed on 2026-08-22 and wrote a temporary screenshot at `/var/folders/ws/_n4r86nj4n18kd2hn5xh43s00000gn/T/meshanvil-viewer-smoke.png`.
- `git status --short` and `git ls-files work viewer | rg 'smoke|png|renders|work/viewer' || true` confirmed no generated browser artefact is tracked.

# Report
- Implemented in `056e927`: `make viewer-smoke` now regenerates the Blender fixture, builds the file-based viewer, injects a minimal browser assertion script, verifies Compare tab, outliner filter, native wipe value and Properties rail selection, and captures the result in a temporary screenshot.
- The smoke found and fixed a real regression: after selecting Compare, `.app[data-workspace]` was stealing subsequent clicks. The click handler now only treats `role=tab` workspace controls as workspace switches.
- The task remains `In progress` only because the current Logics topology still links the orchestration task and promoted leaf tasks to the same backlog items, making automatic closeout unreliable.

# Links
- Request: `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# Evidence
- AC1 | date: 2026-08-22 | command: `make viewer-smoke` | result: passed | make viewer-smoke regenerates the fixture, builds the local viewer, opens it in Chrome headless, checks the pass marker and writes a temporary screenshot.
- AC2 | date: 2026-08-22 | command: `make viewer-smoke` | result: passed | The injected browser smoke changes to Compare, filters the outliner to the voxel row, selects that report, sets the native wipe range to 72 and verifies the rail selection.
- AC3 | date: 2026-08-22 | command: `git status --short; git ls-files work viewer | rg 'smoke|png|renders|work/viewer' || true` | result: passed | git status showed only source and Logics files changed after the smoke; no work/viewer, render or screenshot artefact is tracked.

# AC Traceability
- request-AC6 -> This task. Proof: `056e927`; `make viewer-smoke` passed, exercised Compare, filter, native wipe and rail controls in Chrome, and left screenshots outside the repository.

## task_015_complete_the_mockup_review_controls_without_weakening_the_local_page_boundary - Complete the mockup review controls without weakening the local page boundary
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 95%
> Confidence: 90%
> Progress: 95%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 01:55:25

# AI Context
- Summary: Add filter, labelled native comparison and no-data guidance without persisting state or expanding viewer authority.
- Keywords: complete, mockup, review, controls, weakening, local, page, boundary
- Use when: Implementing the remaining local review controls.
- Skip when: Changing workspace navigation or browser smoke coverage.

# Definition of Done (DoD)
- [x] The backlog scope is implemented.
- [x] Acceptance criteria are covered.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_015_complete_the_mockup_review_controls_without_weakening_the_local_page_boundary`

# Acceptance criteria
- AC1: Filtering is reversible and hides only nonmatching visible rows.
- AC2: The comparison divider remains draggable and keyboard-adjustable while before/after labels identify the two states.
- AC3: First run describes a valid next command and every displayed environment state has an explanation.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_015_complete_the_mockup_review_controls_without_weakening_the_local_page_boundary.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_015_complete_the_mockup_review_controls_without_weakening_the_local_page_boundary.md` after implementation.

# Validation
- `make check` passed on 2026-08-22: compile, JSDoc types, selfcheck, i18n and hygiene.
- `make fixture` passed on 2026-08-22: real Blender fixture regenerated four reports.
- `./bin/meshanvil view --no-open` built `work/viewer/index.html` from the generated reports.
- Chrome headless wrote `/tmp/meshanvil-viewer-task015.png`; the rendered page shows the Properties rail and no static black strip below the Image Editor.

# Report
- Implemented the remaining review controls in `1d888c3`: the runbook workspace now obeys the local outliner filter, Properties has a section rail for Input, Measurements and Links, and the first-run/state explanations remain driven by existing doctor and report data.
- The task remains `In progress` only because the current Logics topology still links the orchestration task and promoted leaf tasks to the same backlog items, which makes automatic closeout unreliable. No acceptance evidence is intentionally missing for this task.

# Links
- Request: `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# Evidence
- AC1 | date: 2026-08-22 | command: `make check` | result: passed | The outliner filter matches report IDs, operation names and runbook titles without mutating report data.
- AC2 | date: 2026-08-22 | command: `make check; make fixture` | result: passed | The native range comparison keeps keyboard adjustment and now labels before and after states visibly.
- AC1 | date: 2026-08-22 | command: `make check; Chrome headless screenshot /tmp/meshanvil-viewer-task015.png` | result: passed | The outliner filter now applies in both chain and runbook workspaces, and the report rail jumps to existing rendered sections without persisting UI state.
- AC3 | date: 2026-08-22 | command: `make check; make fixture; ./bin/meshanvil view --no-open` | result: passed | The first-run properties use local doctor and ops data only: setup, reports and contributor-tool states each include an explanation plus a valid command fallback.

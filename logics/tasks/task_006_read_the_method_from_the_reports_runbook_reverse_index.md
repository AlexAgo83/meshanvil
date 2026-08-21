## task_006_read_the_method_from_the_reports_runbook_reverse_index - Read the method from the reports: runbook reverse index
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 99%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 01:11:06

# AI Context
- Summary: Derive runbook coverage at view time from report `links.docs`; preserve full slugs and use the existing Logics metadata bridge.
- Keywords: read, method, reports, runbook, reverse, index
- Use when: Tracing an operation to its method or a runbook to the operations that applied it.
- Skip when: Editing the report links or rendering a Logics document.

# Definition of Done (DoD)
- [x] The backlog scope is implemented.
- [x] Acceptance criteria are covered.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_008_read_the_method_from_the_reports_runbook_reverse_index`

# Acceptance criteria
- AC1: For each runbook, the operations that cite it are listed, derived from the reports and from nothing else.
- AC2: A runbook cited by no operation is shown as not yet applied.
- AC3: Chips use the Logics prefixes and hues, with the runbook prefix N as that convention requires.
- AC4: A chip navigates in both directions between an operation and a document.
- AC5: The file keeps the full slug; the chip is a rendering, never a storage format.

# Plan
- [x] Use `python3 -m logics_manager flow progress task task_006_read_the_method_from_the_reports_runbook_reverse_index.md --progress <n>%` during multi-wave work.
- [x] Run `python3 -m logics_manager flow finish task task_006_read_the_method_from_the_reports_runbook_reverse_index.md` after implementation.

# Validation
- `make check`
- `./bin/meshanvil view --no-open`
- `node --check viewer/viewer.js`
- `git diff --check`

# Report
- Added a view-time reverse index over report links and bidirectional operation/runbook navigation.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# Evidence
- AC1 | date: 2026-08-22 | command: `meshanvil view --no-open` | result: passed | Viewer build derives runbook coverage from report links and keeps unreferenced runbooks in the payload.

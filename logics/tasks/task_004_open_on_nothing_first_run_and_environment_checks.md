## task_004_open_on_nothing_first_run_and_environment_checks - Open on nothing: first run and environment checks
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 98%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 00:43:44

# AI Context
- Summary: The viewer reads `work/doctor.json` and `work/ops` only; it never starts checks or operations.
- Keywords: open, nothing, first, run, environment, checks
- Use when: Opening the viewer before any operation report exists.
- Skip when: Reviewing an existing operation chain.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_006_open_on_nothing_first_run_and_environment_checks`

# Acceptance criteria
- AC1: With no report present, the tool states what it can do and the command that produces the first report.
- AC2: The environment check names the Blender binary and version it will use, or says it did not find one and how to point at it.
- AC3: A missing work/ops is reported as not yet created, not as an error.
- AC4: No area of the interface is blank without an explanation of what would fill it.
- AC5: The start screen can be reopened after the first run, so the checks stay reachable.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_004_open_on_nothing_first_run_and_environment_checks.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_004_open_on_nothing_first_run_and_environment_checks.md` after implementation.

# Validation
- `make check`
- `make fixture`
- `MESHANVIL_LANG=fr ./bin/meshanvil view --no-open`
- `node --check viewer/viewer.js`
- `git diff --check`

# Report
- Added a reopenable Start screen with the demo, inspection, and printable-body commands.
- The screen reads the last doctor report, calls a missing `work/ops` normal, and explains each editor area.
- Code delivery is complete. `flow closeout` remains blocked by root-request AC proof placeholders outside this slice.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

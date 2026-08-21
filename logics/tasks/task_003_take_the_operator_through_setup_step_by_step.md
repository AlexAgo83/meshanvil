## task_003_take_the_operator_through_setup_step_by_step - Take the operator through setup, step by step
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 60%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 00:30:00

# AI Context
- Summary: Add a cached, machine-readable setup check for Blender, optional FreeCAD, and the writable workspace; later screens consume its report.
- Keywords: take, operator, through, setup, step
- Use when: Adding setup requirements, engine discovery, version floors, or the shared first-run diagnostic report.
- Skip when: Rendering the empty viewer itself; item_006 consumes this report.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_012_take_the_operator_through_setup_step_by_step`

# Acceptance criteria
- AC1: One command reports every requirement with its state, its version where one exists, and whether it is required, optional or contributor-only.
- AC2: A missing or too-old engine is named as such, with the version found, the version needed, and the override variable -- never as a failure raised from inside an operation.
- AC3: Blender below 4.2 is refused before an operation starts, naming the operator that requires it.
- AC4: FreeCAD absent is reported as optional, and every Blender operation keeps working.
- AC5: Node and logics-manager are never presented as requirements for running an operation.
- AC6: The check emits a machine-readable result, and the first-run screen renders that result rather than duplicating the list.
- AC7: Every proposed fix is a command shown for the platform in front of the operator; nothing is installed or modified.
- AC8: work/ is checked for writability and free space before a long operation starts.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_003_take_the_operator_through_setup_step_by_step.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_003_take_the_operator_through_setup_step_by_step.md` after implementation.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

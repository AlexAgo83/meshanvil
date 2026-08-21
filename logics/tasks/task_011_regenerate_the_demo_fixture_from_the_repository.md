## task_011_regenerate_the_demo_fixture_from_the_repository - Regenerate the demo fixture from the repository
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 95%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 00:59:36

# AI Context
- Summary: The checked-in fixture scripts generate only ignored `work/` data and verify the known defect findings and preserved failed branch.
- Keywords: regenerate, demo, fixture, repository
- Use when: Demonstrating or validating the operation loop without private geometry.
- Skip when: Testing the unversioned STEP import path.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_007_regenerate_the_demo_fixture_from_the_repository`

# Acceptance criteria
- AC1: A single command regenerates the scene, and the same command twice produces the same geometry.
- AC2: tools/scan_defects.py reports the built-in smear and the built-in duplicates without being pointed at them.
- AC3: The chain replays end to end on the generated scene and prints the measurements each step took.
- AC4: A coarse-voxel attempt is kept as a failure with its numbers, since it is the trap run_006 records.
- AC5: Nothing generated is committed, and the publication-hygiene gate still passes.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_011_regenerate_the_demo_fixture_from_the_repository.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_011_regenerate_the_demo_fixture_from_the_repository.md` after implementation.

# Validation
- `make fixture` regenerates the scene and replays the chain from repository scripts
- `make check` confirms no generated data is tracked

# Report
- Confirmed the existing fixture covers deterministic scripted generation, unaided defect discovery, a coarse failed voxel attempt, and ignored outputs.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

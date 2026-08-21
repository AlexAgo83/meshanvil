## task_007_compare_two_states_of_the_same_geometry - Compare two states of the same geometry
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-22 00:51:31

# AI Context
- Summary: The report must declare a same-subject render pair; the viewer presents it with one persistent, accessible wipe position and numeric deltas.
- Keywords: compare, two, states, same, geometry
- Use when: Reviewing a transform whose input and output can share a camera.
- Skip when: Comparing unrelated source files or inferring pairs from render names.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_005_compare_two_states_of_the_same_geometry`

# Acceptance criteria
- AC1: A comparison uses one camera for both states: swapping the images changes the geometry on screen and nothing else.
- AC2: Both states are available in each canonical direction, and switching direction keeps the wipe position.
- AC3: The wipe is draggable with a pointer and movable with the keyboard, and states its position to assistive technology.
- AC4: The numeric difference is shown beside the images, with the axes that moved marked.
- AC5: An operation with no comparable pair says so and names the command that would produce one, rather than showing an empty frame.
- AC6: The report lists its comparable pairs; the viewer reads that list and does not infer it from filenames.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_007_compare_two_states_of_the_same_geometry.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_007_compare_two_states_of_the_same_geometry.md` after implementation.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

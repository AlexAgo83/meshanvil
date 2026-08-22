## item_005_compare_two_states_of_the_same_geometry - Compare two states of the same geometry
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:01:54

# AI Context
- Summary: Two states of one subject rendered on an identical camera, wiped against each other in each canonical view, with the numeric difference beside them.
- Keywords: visual comparison, identical camera, wipe, canonical views, input state render
- Use when: Deciding how an operator sees what an operation changed, beyond the numbers.
- Skip when: Reading a single state -- that is the image editor in item_003.

# Problem
- A voxel at 30 mm destroyed the trims and the feet of the demo part while the volume moved by 3.1% and every topology check stayed green on both sides. The numbers were nearly silent; the image was not.
- Renders are produced per operation on a camera derived from that operation's own result, so two consecutive renders frame differently and cannot be compared.
- Nothing renders the state an operation received, only the state it produced, so there is no before image to compare against.

# Scope
- In:
  - A fixed-camera render mode: the camera is computed once for a subject and reused for every state of it, so only the geometry differs between two images.
  - Rendering the input state as well as the output, on that same camera, for operations that declare a comparison.
  - The four canonical directions on both states: 3/4, front, side, top, plus bottom where an opening is only visible from below.
  - A wipe between the two images, draggable and keyboard-operable, with the view selectable.
  - The numeric difference shown beside the images, with the axes that moved marked.
  - The report recording which pairs are comparable, so the viewer never guesses.
- Out:
  - Any comparison across different subjects, or across two unrelated files.
  - Automatic detection of what changed inside an image. The operator reads it; the numbers are next to it.
  - Video, animation or turntable output.

# Acceptance criteria
- AC1: A comparison uses one camera for both states: swapping the images changes the geometry on screen and nothing else.
- AC2: Both states are available in each canonical direction, and switching direction keeps the wipe position.
- AC3: The wipe is draggable with a pointer and movable with the keyboard, and states its position to assistive technology.
- AC4: The numeric difference is shown beside the images, with the axes that moved marked.
- AC5: An operation with no comparable pair says so and names the command that would produce one, rather than showing an empty frame.
- AC6: The report lists its comparable pairs; the viewer reads that list and does not infer it from filenames.

# AC Traceability
- request-AC11 -> This backlog slice. Proof: AC1: A comparison uses one camera for both states: swapping the images changes the geometry on screen and nothing else.
- request-AC2 -> This backlog slice, partially. Proof: AC4: The numeric difference is shown beside the images, with the axes that moved marked.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: `adr_001_operation_report_format`
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): `adr_001_operation_report_format`
- Request: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`
- Primary task(s): (none yet)

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_000_make_every_3d_operation_reviewable_without_reopening_blender` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`.
- Generated locally by logics-manager.
- Task `task_007_compare_two_states_of_the_same_geometry` was finished via `logics-manager flow finish task` on 2026-08-22.

# Tasks
- `task_007_compare_two_states_of_the_same_geometry`

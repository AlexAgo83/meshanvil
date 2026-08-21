## item_012_take_the_operator_through_setup_step_by_step - Take the operator through setup, step by step
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 45%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 00:25:32

# AI Context
- Summary: One check that names every requirement, says which are required, optional or contributor-only, and gives the exact fix for the platform in front of it -- printing commands, never installing.
- Keywords: setup, doctor, prerequisites, engine version floor, guided fix
- Use when: Deciding what the tool requires, how it reports a missing requirement, or how someone gets from a clone to a first report.
- Skip when: Reporting the state of a chain -- that is the first-run screen in item_006, which renders what this produces.

# Problem
- Getting from a clone to a first report is undocumented and unassisted. The measured platforms make that worse: Blender is not on PATH on Windows, absent from Linux in WSL, and behind an application bundle on macOS.
- Nothing states a minimum Blender version, yet the pipeline calls `bpy.ops.wm.stl_export`, which exists only from 4.2 -- earlier versions used a different operator and would fail deep inside an operation rather than at the start.
- The requirements are not of one kind, and treating them alike misleads. Blender is required. FreeCAD is needed only to read a STEP source. Node and logics-manager are for contributors and have no business being asked of someone who came to prepare a mesh.
- A failed prerequisite currently surfaces as whatever error the engine happens to raise, at whatever depth it happens to fail.

# Scope
- In:
  - A single check -- `meshanvil doctor` -- listing every requirement with its state: found with its version, found but too old, missing, or not needed for what you are doing.
  - Requirements classified as required, optional or contributor-only, with the reason each one exists stated in a sentence.
  - A version floor per engine, checked and named: Blender 4.2 or later, derived from the operators the pipeline calls; FreeCAD 1.0, the version verified.
  - A fix for the platform in front of the operator: where the engine usually lives, which environment variable overrides it, and the command to run -- printed, never executed, as `adr_003_the_viewer_reads_the_command_acts` requires.
  - The check emitting a machine-readable result, so the CLI and the first-run screen of `item_006` render the same source rather than each maintaining its own list.
  - The result cached against the engine path and its modification time, so a check that costs a subprocess is not repeated on every command.
  - A guided order: the check stops at the first blocker, states it, and is re-runnable until it passes.
  - Writability and space checks on work/, since an operation that runs for fifteen minutes and cannot write its output is the worst way to learn it.
- Out:
  - Installing, downloading or unpacking anything. The tool prints what to run and the operator runs it.
  - Modifying PATH, shell profiles or system configuration.
  - Bundling an engine, or vendoring Blender.
  - A graphical installer.

# Acceptance criteria
- AC1: One command reports every requirement with its state, its version where one exists, and whether it is required, optional or contributor-only.
- AC2: A missing or too-old engine is named as such, with the version found, the version needed, and the override variable -- never as a failure raised from inside an operation.
- AC3: Blender below 4.2 is refused before an operation starts, naming the operator that requires it.
- AC4: FreeCAD absent is reported as optional, and every Blender operation keeps working.
- AC5: Node and logics-manager are never presented as requirements for running an operation.
- AC6: The check emits a machine-readable result, and the first-run screen renders that result rather than duplicating the list.
- AC7: Every proposed fix is a command shown for the platform in front of the operator; nothing is installed or modified.
- AC8: work/ is checked for writability and free space before a long operation starts.

# AC Traceability
- request-AC24 -> This backlog slice. Proof: AC1: One command reports every requirement with its state, its version where one exists, and whether it is required, optional or contributor-only.
- request-AC12 -> This backlog slice, partially. Proof: AC6: the first-run screen renders the check's result rather than duplicating the list.
- request-AC19 -> This backlog slice, partially. Proof: AC2: A missing or too-old engine is named before an operation starts, not raised from inside one.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: `adr_004_target_technology_and_process_model`, `adr_003_the_viewer_reads_the_command_acts`
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): `adr_004_target_technology_and_process_model`, `adr_003_the_viewer_reads_the_command_acts`
- Request: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`
- Primary task(s): (none yet)

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_000_make_every_3d_operation_reviewable_without_reopening_blender` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`.
- Generated locally by logics-manager.

# Tasks
- `task_003_take_the_operator_through_setup_step_by_step`

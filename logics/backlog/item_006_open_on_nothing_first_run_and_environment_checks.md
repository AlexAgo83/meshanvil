## item_006_open_on_nothing_first_run_and_environment_checks - Open on nothing: first run and environment checks
> From version: 1.0.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:11:06

# AI Context
- Summary: The first launch, when work/ops is empty: what the tool can do, what it found in its environment, and the command that writes the first report.
- Keywords: first run, empty state, environment check, Blender path, onboarding
- Use when: Working on what someone sees before any operation has run.
- Skip when: Working on a populated chain -- item_003 covers that.

# Problem
- On a first launch there is no report, so every area of the interface is empty and nothing says what to do.
- The first real failure on another machine is Blender not being where the tool expects, and nothing checks it before an operation fails.
- Someone arriving with no 3D source of their own has nothing to try the tool on.

# Scope
- In:
  - A start screen listing what a first chain can be: inspect a source, sweep for export defects, prepare a printable body -- each showing the command it runs.
  - Rendering the result of `meshanvil doctor` (item_012) rather than checking anything itself: one list, two surfaces.
  - Environment checks stated plainly: the Blender binary and its version, the pinned logics-manager, whether work/ops exists yet, and Mermaid available offline.
  - The override named where it is needed: the environment variable that points at another Blender.
  - A pointer to the generated demo scene for someone with no source of their own.
  - Every area of the empty interface saying what would fill it, and the command that does.
- Out:
  - Installing anything, including Blender.
  - A configuration screen. The one override is an environment variable, stated where it matters.
  - Deciding what the requirements are or how they are checked: that is item_012, and this slice only displays what it produces.
  - Telemetry, first-run tracking, or any network call.

# Acceptance criteria
- AC1: With no report present, the tool states what it can do and the command that produces the first report.
- AC2: The environment check names the Blender binary and version it will use, or says it did not find one and how to point at it.
- AC3: A missing work/ops is reported as not yet created, not as an error.
- AC4: No area of the interface is blank without an explanation of what would fill it.
- AC5: The start screen can be reopened after the first run, so the checks stay reachable.

# AC Traceability
- request-AC12 -> This backlog slice. Proof: AC1: With no report present, the tool states what it can do and the command that produces the first report.
- request-AC14 -> This backlog slice, partially. Proof: AC1: the start screen shows commands rather than running them.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: `adr_003_the_viewer_reads_the_command_acts`
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): `adr_003_the_viewer_reads_the_command_acts`
- Request: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`
- Primary task(s): (none yet)

# Priority
- Priority: Medium
- Rationale: Default until groomed.

# Notes
- Hybrid rationale: Derived from request `req_000_make_every_3d_operation_reviewable_without_reopening_blender` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_000_make_every_3d_operation_reviewable_without_reopening_blender.md`.
- Generated locally by logics-manager.
- Task `task_004_open_on_nothing_first_run_and_environment_checks` was finished via `logics-manager flow finish task` on 2026-08-22.

# Tasks
- `task_004_open_on_nothing_first_run_and_environment_checks`

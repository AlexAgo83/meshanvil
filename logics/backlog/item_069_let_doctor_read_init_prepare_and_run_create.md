## item_069_let_doctor_read_init_prepare_and_run_create - Let doctor read, init prepare, and run create
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 80%
> Complexity: Low
> Theme: Installation and first run
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 12:30:45

# AI Context
- Summary: Stop `doctor` creating `work/`: a check reports, `init` prepares, and `run` creates what it is about to write.
- Keywords: doctor side effect, work directory, read-only check, run precondition
- Use when: changing where the work directory is created and what refuses when it is missing.
- Skip when: changing engine discovery or the doctor report shape.

# Problem
- `doctor.work()` calls `mkdir` before probing for writability. `doctor` is the command the README hands a new user first, so running it in a home directory to check whether Blender was found leaves a `work/` and a `work/doctor.json` behind.
- A check that creates what it was asked to look at cannot report that it is missing, and the `mkdir` fix string it already carries is unreachable.

# Scope
- In:
  - `doctor.work()` probes the parent for writability and reports `missing` with its existing fix rather than creating the directory.
  - `runner.run` creates what it is about to write, as it already does for `work/ops`, so an uninitialised directory still produces one report rather than one refusal.
  - One selfcheck asserting `doctor` leaves an empty directory empty, and that `run` still succeeds there.
- Out:
  - Changing `init`, which already creates the work directories.
  - Changing the exit codes.
  - Making `run` create a project marker: an unmarked directory is still the project by the current-directory rule.

# Acceptance criteria
- AC4: `meshanvil doctor` does not create directories. A missing `work/` is reported as missing with its existing `mkdir` fix, and the `run` refusal path is adjusted in the same change so an uninitialised project still gives one actionable message.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC4: `meshanvil doctor` does not create directories. A missing `work/` is reported as missing with its existing `mkdir` fix, and the `run` refusal path is adjusted in the same change so an uninitialised project still gives one actionable message.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: Not needed
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)
- Request: `req_015_make_a_fresh_installation_reach_its_first_report`
- Primary task(s): `task_028_deliver_a_first_run_path_a_fresh_installation_can_walk`

# Priority
- Priority: Medium
- Rationale: Small and self-contained, but it changes a refusal path, so it wants its own slice rather than riding along with another.

# Notes
- Hybrid rationale: Derived from request `req_015_make_a_fresh_installation_reach_its_first_report` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_015_make_a_fresh_installation_reach_its_first_report.md`.
- Generated locally by logics-manager.

# Tasks
- `task_028_deliver_a_first_run_path_a_fresh_installation_can_walk`

## item_070_point_the_readme_installation_at_a_route_that_works_today - Point the README installation at a route that works today
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
- Summary: Replace the README's `pip install meshanvil` with the repository install that works today, and say plainly that PyPI comes at 1.0.
- Keywords: README, install command, PyPI, pre-1.0 honesty
- Use when: correcting the documented installation route.
- Skip when: preparing or publishing a PyPI release.

# Problem
- `python -m pip install meshanvil` is the first command in the README's installation section and returns 404: the name is not on PyPI. Every reader who follows the documented path stops on line one.

# Scope
- In:
  - The installation section installs from the repository and states that PyPI is deferred to 1.0.
  - The contributor route (`clone`, `./bin/meshanvil`) stays as it is.
- Out:
  - Claiming the PyPI name or preparing a release: decided against for a pre-1.0 tool.
  - Restructuring the README.

# Acceptance criteria
- AC1: The documented installation command works as written. Decided: the README installs from the repository (`pip install git+https://github.com/AlexAgo83/meshanvil`) and says so plainly; PyPI is deferred to 1.0 rather than claimed for a pre-1.0 tool.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: The documented installation command works as written. Decided: the README installs from the repository (`pip install git+https://github.com/AlexAgo83/meshanvil`) and says so plainly; PyPI is deferred to 1.0 rather than claimed for a pre-1.0 tool.

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
- Priority: High
- Rationale: A one-line correction on the first command a new reader runs.

# Notes
- Hybrid rationale: Derived from request `req_015_make_a_fresh_installation_reach_its_first_report` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_015_make_a_fresh_installation_reach_its_first_report.md`.
- Generated locally by logics-manager.

# Tasks
- `task_028_deliver_a_first_run_path_a_fresh_installation_can_walk`

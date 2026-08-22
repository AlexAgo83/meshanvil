## item_049_give_the_host_code_a_test_layout_with_one_module_per_host_module - Give the host code a test layout with one module per host module
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:37:31

# AI Context
- Summary: A test directory and runner with one test module per host module, carrying over what the single selfcheck script asserts today, plus smoke coverage of live refresh.
- Keywords: test layout, per-module tests, selfcheck migration, smoke coverage
- Use when: Adding or reorganising checks over the host code.
- Skip when: Adding client-side unit tests, which stay out of this pass.

# Problem
- `scripts/selfcheck.py` is 353 lines of hand-rolled asserts covering every host module at once, so no module has a place of its own to be checked and a failure names the script rather than the unit.

# Scope
- In:
  - A test directory and a runner, wired into `make check` as the same entry point it is today.
  - One test module per host module, carrying over what `scripts/selfcheck.py` already asserts.
  - Extending `scripts/viewer_smoke.py` over the live-refresh path.
- Out:
  - Client-side unit tests.
  - Coverage thresholds; a gate to argue with before there is anything to gate.

# Acceptance criteria
- AC1: `make check` runs the test suite and a failure names the failing unit.
- AC2: Every host module has a test module, and nothing `scripts/selfcheck.py` asserted today is lost.
- AC3: The smoke suite passes against the restructured client and server and covers the live-refresh path.

# AC Traceability
- request-AC10 -> This backlog slice. Proof: AC1: `make check` runs the test suite and a failure names the failing unit.
- request-AC11 -> This backlog slice. Proof: AC2: Every host module has a test module, and nothing `scripts/selfcheck.py` asserted today is lost.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_011_a_viewer_that_stays_current_and_a_codebase_that_stays_divisible`
- Architecture decision(s): (none yet)
- Request: `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`
- Primary task(s): `task_024_deliver_the_live_viewer_and_the_module_structure`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.

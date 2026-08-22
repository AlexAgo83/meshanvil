## item_049_give_the_host_code_a_test_layout_with_one_module_per_host_module - Give the host code a test layout with one module per host module
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 60%
> Complexity: Medium
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:08:22

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

# Implementation anchors
> Line numbers read at `50e5b00`; treat them as a starting point, not a contract -- the named function or literal is the anchor that survives an edit.

- `scripts/selfcheck.py` is 353 lines holding 18 checks that already map onto modules: `check_parameters` `:17`, `check_identity` `:36`, `check_parent` `:53`, `check_projects` `:60`, `check_bbox_delta` `:113`, `check_refusals` `:123`, `check_i18n` `:130`, `check_doctor` `:151`, `check_engine_floor` `:169`, `check_wsl_boundary` `:178`, `check_doctor_exit_code` `:188`, `check_viewer_start` `:198`, `check_run_endpoint` `:211`, `check_viewer_comparison_layout` `:266`, `check_logics_bridge` `:286`, `check_prune` `:298`, `check_target_lock` `:312`, driven by `main()` `:326`. Carrying them over is a move, not a rewrite -- each already takes a `tmp: Path` or nothing.
- `Makefile:12` is `check: compile types selfcheck i18n hygiene`; a test target joins that list and `selfcheck` leaves it once its content has moved.
- `.github/workflows/ci.yml:23` runs `make check` on Python 3.12 after `npm ci`. A runner that is not in the standard library has to be installable there, which is a reason to keep it to one.
- The host is standard-library-only at runtime (`adr_004`); a test runner is a development dependency and must not become an import of `meshanvil/`.

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

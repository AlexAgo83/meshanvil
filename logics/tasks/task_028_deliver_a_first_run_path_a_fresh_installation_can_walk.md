## task_028_deliver_a_first_run_path_a_fresh_installation_can_walk - Deliver a first-run path a fresh installation can walk
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-23 12:38:21

# AI Context
- Summary: Implementation plan for the first-run request, ordered so the check that catches installation defects lands before the slices that could introduce them.
- Keywords: install check, demo command, doctor side effect, README install route
- Use when: delivering req_015 or coordinating its four backlog slices.
- Skip when: working on the agent-facing JSON contract, which is a separate request.

# Context
- Coordinate the AC-aware split backlog items without implementing them directly.
- The request was written from a real walkthrough: the wheel built, installed into a clean venv, and the README followed line by line. Two defects found on that walk are already fixed; these four slices are what it did not cover.
- PyPI was decided against for a pre-1.0 tool. the README slice below documents the route that works today; claiming the name is deferred to 1.0.

# Plan
- [x] 1. `item_067` first: the install check is what catches this whole class of defect, and every slice below is safer once a target fails when the installed command stops working.
- [x] 2. `item_070`: correct the README installation line. One line, and it is the first command a new reader runs.
- [x] 3. `item_069`: move directory creation out of `doctor` and into `run`, with the refusal path adjusted in the same change.
- [x] 4. `item_068`: add the demo command last, once `doctor` no longer creates directories under it and the install check can exercise it.
- [x] 5. Run `make check`, `make install-check`, `make package`, Logics lint, audit and flow validate.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and validation pass.

# Backlog
- `item_067_install_the_wheel_and_run_the_command_in_a_clean_environment`
- `item_068_give_a_fresh_installation_a_subject_it_can_generate_itself`
- `item_069_let_doctor_read_init_prepare_and_run_create`
- `item_070_point_the_readme_installation_at_a_route_that_works_today`

# Definition of Done (DoD)
- [x] Generated backlog slices are linked and ready for implementation.
- [x] Slice ownership and next action are clear.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009 without automatic commits or one commit per micro-step.

# AC Traceability
- request-AC1 -> This task. Proof: README now installs with `python -m pip install git+https://github.com/AlexAgo83/meshanvil` and states PyPI is deferred to 1.0; implemented in `dc4fd86`.
- request-AC2 -> This task. Proof: `meshanvil demo` generates `work/out/demo_figure.blend` from primitives and writes `work/ops/001_scan_defects.json` from a fresh empty directory; validated with a real command run and implemented in `94b9d16`.
- request-AC3 -> This task. Proof: `meshanvil demo` resolves generator scripts through packaged runtime assets, uses the installed command path through the CLI, and writes under `paths.work_root()/work`; `make package` and `make install-check` passed with the demo generators in the wheel; implemented in `94b9d16`.
- request-AC4 -> This task. Proof: `doctor.work` no longer creates `work/`; `runner.run` creates the work tree before writing; covered by `check_doctor` and `check_run_creates_work`; implemented in `2b3cbf4`.
- request-AC5 -> This task. Proof: `make install-check` builds a wheel, installs it into a clean virtual environment and runs `meshanvil --version`, the bare welcome and `doctor --json`; implemented in `6dca55f`.
- request-AC6 -> This task. Proof: `make check`, `make package`, `make install-check`, `make release-dry-run`, `logics-manager lint --require-status`, `logics-manager audit --group-by-doc`, and `flow validate` passed.

# Validation
- `python3 -m pytest -q tests/test_doctor.py tests/test_runner.py` passed.
- `python3 -m pytest -q tests/test_cli.py tests/test_i18n.py` passed.
- `python3 scripts/selfcheck.py` passed.
- `make check` passed: 28 pytest tests, i18n and hygiene.
- `make package` passed: package assets OK, 42 files.
- `make install-check` passed.
- `meshanvil demo` passed from a fresh temporary directory and wrote `work/ops/001_scan_defects.json`.
- `make release-dry-run` passed.
- `logics-manager lint --require-status` passed.
- `logics-manager audit --group-by-doc` passed with only deferred closeout warnings.
- `logics-manager flow validate task_028_deliver_a_first_run_path_a_fresh_installation_can_walk` passed.
- Implemented in 6dca55f, dc4fd86, 2b3cbf4 and 94b9d16. Passed: pytest doctor/runner, pytest cli/i18n, scripts/selfcheck.py, make check, make package, make install-check, real meshanvil demo from a fresh temp directory, make release-dry-run, logics lint, audit and flow validate.
- Finish workflow executed on 2026-08-23.
- Linked backlog/request close verification passed.

# Report
- Added `scripts/install_check.py`, `make install-check`, and wired it into `release-dry-run`.
- Corrected the README install command to the repository URL and explicitly deferred PyPI to 1.0.
- Made `doctor` read-only for missing `work/`, while `run` creates the work tree it is about to write.
- Added `meshanvil demo [figure|vehicle]`, backed by the existing primitive generators and a first `scan_defects` report.
- Updated the package asset check, CLI help text and locales for the demo command.
- Finished on 2026-08-23.
- Linked backlog item(s): `item_067_install_the_wheel_and_run_the_command_in_a_clean_environment`, `item_068_give_a_fresh_installation_a_subject_it_can_generate_itself`, `item_069_let_doctor_read_init_prepare_and_run_create`, `item_070_point_the_readme_installation_at_a_route_that_works_today`
- Related request(s): `req_015_make_a_fresh_installation_reach_its_first_report`

# Links
- Request: `req_015_make_a_fresh_installation_reach_its_first_report`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

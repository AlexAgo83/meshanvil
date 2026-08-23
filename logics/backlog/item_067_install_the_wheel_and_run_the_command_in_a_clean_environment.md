## item_067_install_the_wheel_and_run_the_command_in_a_clean_environment - Install the wheel and run the command in a clean environment
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 20%
> Complexity: Low
> Theme: Installation and first run
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 12:30:45

# AI Context
- Summary: Add a check that installs the built wheel into a throwaway environment and runs the console script, so a broken installation fails a target instead of a user.
- Keywords: install check, wheel, clean venv, console script, smoke test
- Use when: adding or changing the check that exercises meshanvil as an installed package.
- Skip when: changing what the wheel contains; that is `scripts/check_package.py` and `pyproject.toml`.

# Problem
- Nothing exercises meshanvil as an installed package. `make check` inspects the source tree and `scripts/check_package.py` inspects the wheel's file list; neither installs the wheel and runs the command.
- That blind spot is not theoretical: it hid a `fix_command` hint that offered a WSL path on macOS, and a set of contributor shell scripts that shipped in the wheel, wrote a generated `.blend` into `site-packages`, failed on every CLI call and still exited 0.

# Scope
- In:
  - A `make install-check` target: build the wheel, install it into a throwaway virtual environment, run the console script, remove the environment.
  - Assertions on `meshanvil --version`, the bare welcome, and `doctor --json` parsing as one JSON object.
  - Wiring it into `release-dry-run`, where a slow target belongs.
- Out:
  - Adding it to `make check`: building and installing a wheel per run is too slow for the loop developers stay in.
  - Running an operation, which needs Blender and a source.
  - Testing more than one Python version or platform.

# Acceptance criteria
- AC5: A check installs the built wheel into a clean environment and asserts the console script runs: `--version`, the bare welcome, and `doctor --json` parsing as JSON. It fails if an installed command no longer starts.
- AC6: `make check`, `make package`, `logics-manager lint --require-status` and `logics-manager audit --group-by-doc` pass.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC5: A check installs the built wheel into a clean environment and asserts the console script runs: `--version`, the bare welcome, and `doctor --json` parsing as JSON. It fails if an installed command no longer starts.
- request-AC6 -> This backlog slice. Proof: AC6: `make check`, `make package`, `logics-manager lint --require-status` and `logics-manager audit --group-by-doc` pass.

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
- Rationale: It is the check that would have caught both defects already fixed in this area, and it guards every slice below.

# Notes
- Hybrid rationale: Derived from request `req_015_make_a_fresh_installation_reach_its_first_report` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_015_make_a_fresh_installation_reach_its_first_report.md`.
- Generated locally by logics-manager.

# Tasks
- `task_028_deliver_a_first_run_path_a_fresh_installation_can_walk`

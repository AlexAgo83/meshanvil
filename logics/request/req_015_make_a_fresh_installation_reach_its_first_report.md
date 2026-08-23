## req_015_make_a_fresh_installation_reach_its_first_report - Make a fresh installation reach its first report
> From version: 0.1.0
> Schema version: 1.0
> Status: Draft
> Understanding: 85
> Confidence: 80
> Complexity: Medium
> Theme: Installation and first run
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.

# AI Context
- Summary: Close the gap between `pip install meshanvil` and a first report: a published package, something to run an operation on, and a `doctor` that does not create directories where it was only asked to look.
- Keywords: installation, first run, PyPI, onboarding, sample source, doctor side effect
- Use when: working on what a new user meets between installing the tool and reading their first report.
- Skip when: changing operation semantics, viewer presentation, or the agent-facing JSON contract, which is scoped separately.

# Needs
- `python -m pip install meshanvil` is the first command in the README and returns 404: the name is not on PyPI. Every reader who follows the documented path stops on line one. Either the package is published, or the README states the real installation route until it is.
- A fresh installation has a working CLI, a `doctor` that passes, ten operations in `meshanvil list`, and nothing to run any of them on. Every operation needs a `.blend`, `.obj`, `.stl`, `.ply` or `.step` source the user must already own. The tool cannot demonstrate itself, so the first report is gated on the user having a 3D file and knowing which operation suits it.
- `tools/make_demo_vehicle.py` and `tools/make_demo_figure.py` already generate a subject from primitives with no donor file and nothing to license, and both ship in the wheel. What is missing is a command that reaches them: the shell chains that used to call them resolved `bin/meshanvil` and `fixtures/` from their own parent and were removed from the wheel because neither is packaged.
- `meshanvil doctor` creates `work/` before probing it for writability. It is the command the README tells a new user to run first, so running it in a home directory to check whether Blender was found leaves a `work/` and a `work/doctor.json` behind. A check should report that the directory is missing and offer the `mkdir` fix it already carries, not create it.
- Nothing verifies the installed package from outside the checkout. `make check` and `scripts/check_package.py` inspect the tree and the wheel's file list; neither installs the wheel into a clean environment and runs the command. That is the gap the two defects fixed alongside this request both hid in.

# Context
- Keep this about installation and first run. The agent-facing JSON contract is scoped by its own request and is not in scope here.
- No new runtime dependency and no downloaded asset: a generated subject is the only kind this project can ship, and both generators already exist.
- Publishing to PyPI is an operator decision with a name to claim and a release to sign. This request records the gap; it does not assume the answer.
- Changing `doctor` to stop creating `work/` changes what `run` sees in an uninitialised directory, since `run` refuses when `doctor.work(root)["state"] != "found"`. Decide the pair together.
- Generated and runtime data under `work/` is not versioned. Demonstration output belongs under the project's own `work/`, never beside the installed package.

# Acceptance criteria
- AC1: The documented installation command works as written. Either `meshanvil` resolves on PyPI, or the README's installation section names the route that does until it is published.
- AC2: A new user with no 3D file of their own can produce a first report with commands from the README alone, using a subject the tool generates from primitives.
- AC3: Whatever exposes that subject is reachable from an installed package: it resolves the CLI through the installed console script and writes only under the active project's `work/`, never beside the installed package.
- AC4: `meshanvil doctor` does not create directories. A missing `work/` is reported as missing with its existing `mkdir` fix, and the `run` refusal path is adjusted in the same change so an uninitialised project still gives one actionable message.
- AC5: A check installs the built wheel into a clean environment and asserts the console script runs: `--version`, the bare welcome, and `doctor --json` parsing as JSON. It fails if an installed command no longer starts.
- AC6: `make check`, `make package`, `logics-manager lint --require-status` and `logics-manager audit --group-by-doc` pass.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# References
- README.md
- pyproject.toml
- Makefile
- meshanvil/doctor.py
- meshanvil/paths.py
- meshanvil/runner.py
- tools/make_demo_vehicle.py
- tools/make_demo_figure.py
- tools/build_demo_chain.sh
- scripts/check_package.py
- scripts/selfcheck.py

# Backlog
- none

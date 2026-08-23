## item_068_give_a_fresh_installation_a_subject_it_can_generate_itself - Give a fresh installation a subject it can generate itself
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Installation and first run
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.

# AI Context
- Summary: Add a command that generates a subject from primitives and runs a short chain on it, so a new user reaches a first report without owning a 3D file.
- Keywords: demo command, generated subject, first report, onboarding
- Use when: implementing the command that gives a fresh installation something to run.
- Skip when: changing what the existing operations measure or how reports are shaped.

# Problem
- A fresh installation has a working CLI, a `doctor` that passes and ten operations in `meshanvil list`, and nothing to run any of them on. Every operation needs a source the user must already own, so the first report is gated on having a 3D file and knowing which operation suits it.
- The generators already exist and ship in the wheel: `tools/make_demo_vehicle.py` and `tools/make_demo_figure.py` build a subject from primitives, with no donor file and nothing to license. What is missing is a command that reaches them.
- The shell chains that used to call them resolved `bin/meshanvil` and `fixtures/` from their own parent. Neither is packaged, so installed they wrote into `site-packages` and failed on every CLI call. They are contributor scripts and no longer ship.

# Scope
- In:
  - A `meshanvil demo` command: generate the subject into the active project's `work/`, then run a short chain of existing operations through the existing runner.
  - Everything it writes lands under the active project's `work/`, resolved by `paths`, never beside the installed package.
  - A closing line naming the reports it wrote and `meshanvil view` as the next command.
  - A selfcheck that runs the command with the engine stubbed, asserting where it writes and that it refuses rather than half-runs when Blender is missing.
- Out:
  - Shipping a `.blend` fixture in the wheel: a generator that needs no donor file is already there.
  - A new operation, or new geometry logic of any kind.
  - Restoring the contributor shell chains to the wheel.

# Acceptance criteria
- AC2: A new user with no 3D file of their own can produce a first report with commands from the README alone, using a subject the tool generates from primitives.
- AC3: Whatever exposes that subject is reachable from an installed package: it resolves the CLI through the installed console script and writes only under the active project's `work/`, never beside the installed package.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC2: A new user with no 3D file of their own can produce a first report with commands from the README alone, using a subject the tool generates from primitives.
- request-AC3 -> This backlog slice. Proof: AC3: Whatever exposes that subject is reachable from an installed package: it resolves the CLI through the installed console script and writes only under the active project's `work/`, never beside the installed package.

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
- Rationale: It is the only slice that changes what the product can do for someone who just installed it.

# Notes
- Hybrid rationale: Derived from request `req_015_make_a_fresh_installation_reach_its_first_report` and kept bounded to one coherent delivery slice.
- Source file: `logics/request/req_015_make_a_fresh_installation_reach_its_first_report.md`.
- Generated locally by logics-manager.

# Tasks
- `task_028_deliver_a_first_run_path_a_fresh_installation_can_walk`

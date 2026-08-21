## item_013_bridge_reports_into_the_logics_corpus - Bridge reports into the Logics corpus
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 92%
> Complexity: High
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:09:03

# AI Context
- Summary: Three bridges over the logics-manager CLI: a report recorded as evidence on an acceptance criterion, document chips resolved from the corpus instead of a local table, and a runbook scaffolded from what a chain measured.
- Keywords: evidence bridge, flow evidence add, sync read-doc, runbook scaffold, one-way dependency
- Use when: Connecting an operation's result to the corpus, or resolving a document reference.
- Skip when: Rendering the chain itself, or anything that does not cross into Logics.

# Problem
- A task closeout asks for proof and gets prose, while the measurements that would prove it sit in a report nobody transcribes.
- The viewer's document chips come from a registry written by hand. It holds ten entries today and will be wrong the first time a title changes or a document is renamed.
- Runbooks are written from what a chain established, and their numbers are retyped from a terminal that has scrolled away.
- The two products are published separately, so any bridge that makes one require the other to build or run would break that.

# Scope
- In:
  - `--evidence <task>:<AC>` on the runner: on success, records the proof through `flow evidence add` with the summary, the command as it was actually run, and the report path with its key measurements.
  - Document references resolved through `sync read-doc`: title, kind, status and linked refs read from the corpus, cached for the life of a view, replacing the hand-written registry.
  - A missing or renamed document rendered as missing, never as a stale title.
  - `meshanvil runbook <chain>`: scaffolds through `flow companion runbook`, prefilled with the chain's operations, their parameters, what failed and the numbers that showed it -- the procedure and its limits left for a person to write.
  - Every bridge degrading cleanly when logics-manager is absent: it says so and the operation is unaffected.
  - The Logics viewer URL carried on a chip when one is running, linking out rather than embedding.
- Out:
  - Importing any logics-manager Python module. The bridge is a subprocess and JSON, as `adr_006_bridges_between_meshanvil_and_logics` requires.
  - Writing to the corpus without an explicit flag. An operation is never silently a claim about a task.
  - Rendering Logics documents inside the viewer.
  - Any change to logics-manager itself. If the reverse bridge is ever wanted, it is a request in that repository.

# Acceptance criteria
- AC1: A successful operation run with `--evidence task:AC` appends a proof record carrying the command, the summary and the report path; without the flag the corpus is untouched.
- AC2: A failed operation records no evidence, and says why.
- AC3: Chips render title, kind and status read from the corpus, and a document that no longer exists renders as missing.
- AC4: A chain can scaffold a runbook prefilled with its operations, parameters, failures and numbers, leaving the procedure to be written.
- AC5: With logics-manager absent, operations, reports and the viewer all work, and each bridge states that it is unavailable.
- AC6: No logics-manager module is imported anywhere; every bridge is a subprocess call returning JSON.

# AC Traceability
- request-AC25 -> This backlog slice. Proof: AC1: A successful operation run with `--evidence task:AC` appends a proof record carrying the command, the summary and the report path.
- request-AC15 -> This backlog slice, partially. Proof: AC3: Chips render title, kind and status read from the corpus rather than from a local table.

# Decision framing
- Product framing: Not needed
- Product signals: (none detected)
- Product follow-up: No product brief follow-up is expected based on current signals.
- Architecture framing: `adr_006_bridges_between_meshanvil_and_logics`
- Architecture signals: (none detected)
- Architecture follow-up: No architecture decision follow-up is expected based on current signals.

# Links
- Product brief(s): (none yet)
- Architecture decision(s): `adr_006_bridges_between_meshanvil_and_logics`
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
- `task_005_bridge_reports_into_the_logics_corpus`

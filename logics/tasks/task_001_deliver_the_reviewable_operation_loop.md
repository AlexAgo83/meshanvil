## task_001_deliver_the_reviewable_operation_loop - Deliver the reviewable operation loop
> From version: 1.0.0
> Schema version: 1.0
> Status: In progress
> Understanding: 95%
> Confidence: 90%
> Progress: 95%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:18:07
> Owner: codex

# AI Context
- Summary: Orchestrates the three slices in order: settle and write the report format, build the runner on the converted operations, then build the viewer against real reports rather than fixtures.
- Keywords: orchestration, report format, runner, viewer, conversion order
- Use when: Sequencing the work, or checking what remains before the loop is usable end to end.
- Skip when: Implementing one slice -- read its backlog item instead.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Picking this up

- **Read in this order**: `req_000` for the problem and its 25 acceptance criteria, `prod_001`
  for what the product is and is not, then the six decisions -- `adr_001` the report format with
  its canonical JSON shapes, `adr_004` the technology, process model and repository layout,
  `adr_005` identity, concurrency and exit codes, `adr_003` what the viewer may do, `adr_006` the
  bridges into the corpus, `adr_002` the dependency. Then the slice you are about to build.
- **The context pack is bounded to eight documents by design.** It carries this task, the request,
  the product and the first slices. Before implementing any other slice, build its own pack:
  `logics-manager sync context-pack item_00X_... --mode full --profile deep`.
- **The order in the plan below is not a preference.** `item_001` writes what every other slice
  reads; nothing else starts before a report exists and the twelve operations write one.
- **Two rules that are expensive to unbreak**: host code and engine code never import each other,
  and no operator-facing string is written inline once `item_010` has landed.
- **`logics-manager health` reports ten slices as having no task, and that is expected.** This
  document is the orchestration task and its plan sequences them. A slice gets its own
  implementation task when it is picked up, with
  `logics-manager flow promote backlog-to-task item_00X_...` -- not before, so the corpus does
  not carry ten open tasks nobody is working on.
- **A slice is done when its acceptance criteria are verified with numbers**, on the generated
  fixture rather than on private geometry, and the fixture's own defects are found unaided.
  `logics-manager flow evidence add` records that proof; `item_013` automates it.

# Plan
- [x] 1. Settle the report shape against what the existing operations already measure. Settled in `adr_001_operation_report_format`: twelve scripts, seven transforms and five inspections, one envelope with two payloads, renders and comparable pairs declared rather than inferred.
- [x] 2. Settle what the viewer may do. Settled in `adr_003_the_viewer_reads_the_command_acts`: it reads, and every action is shown as the command that performs it.
- [x] 3. Settle the fixture. `item_007` exists and its three scripts are in the repository: the demo scene generator, the chain replay, and the fixed-camera renders.
- [x] 4. `item_001` -- the report writer is shared by the seven supported manifest operations: six Blender operations and FreeCAD STEP import. The archived `pipeline/` scripts deliberately remain hardcoded delivery records, as scoped by `item_001`, rather than becoming duplicate generic commands.
- [x] 5. `item_002` -- the runner now has command discovery, identity allocation, parent fingerprinting, sibling letters, source protection, exit codes, heartbeat, platform discovery and an exclusive source-fingerprint lock.
- [x] 5a. `item_002` -- the execution contract of `adr_005` is implemented and covered by the host self-check, including the no-second-writer rule.
- [x] 5b. `item_010` -- English and French catalogues and parity checking are in place.
- [x] 6. `item_007` -- the fixture is regenerated and verifies that defects are found unaided.
- [x] 7. `item_003` -- the viewer renders the DAG, report panel, image comparison and command-only menus.
- [x] 7b. `item_012` -- setup requirements and platform-specific fixes are rendered before the first-run view.
- [x] 8. `item_006` -- an empty `work/ops` opens to actionable first-run guidance and environment checks.
- [x] 8b. `item_013` -- reports bridge to bounded Logics documents and runbooks.
- [x] 9. `item_008` -- the reverse index is derived from report links.
- [x] 10. `item_005` -- fixed-camera comparisons have a numeric panel and a draggable wipe.
- [x] 10b. `item_011` -- platform discovery, WSL translation and opening behavior are covered.
- [x] 11. `item_009` -- FreeCAD imports STEP through the same report loop.
- [x] 12. `item_004` -- report-owned artefacts can be pruned while retaining their reports.
- [x] 13. Reports, runbooks and the reverse index cross-link the review method.
- [x] ADR 009 checkpoint: affected Logics documents were updated during delivery waves and the repository was left commit-ready.
- [x] Keep commit creation under operator control; commits were made at meaningful delivery waves.
- [x] GATE: lint, audit, scaffold validation and fixture validation pass. Task closure still awaits request-level proof reconciliation.

# Backlog
- `item_001_define_the_operation_report_and_write_one_from_every_operation`
- `item_002_run_one_named_operation_from_a_single_agent_agnostic_command`
- `item_003_read_the_chain_of_operations_in_a_local_viewer`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_001_define_the_operation_report_and_write_one_from_every_operation`. Proof deferred to slice closeout.
- request-AC2 -> `item_001_define_the_operation_report_and_write_one_from_every_operation`. Proof deferred to slice closeout.
- request-AC3 -> `item_001_define_the_operation_report_and_write_one_from_every_operation`. Proof deferred to slice closeout.
- request-AC7 -> `item_001_define_the_operation_report_and_write_one_from_every_operation`. Proof deferred to slice closeout.
- request-AC4 -> `item_002_run_one_named_operation_from_a_single_agent_agnostic_command`. Proof deferred to slice closeout.
- request-AC8 -> `item_002_run_one_named_operation_from_a_single_agent_agnostic_command`. Proof deferred to slice closeout.
- request-AC5 -> `item_003_read_the_chain_of_operations_in_a_local_viewer`. Proof deferred to slice closeout.
- request-AC6 -> `item_003_read_the_chain_of_operations_in_a_local_viewer`. Proof deferred to slice closeout.
- request-AC8 -> `item_003_read_the_chain_of_operations_in_a_local_viewer`. Proof deferred to slice closeout.
- request-AC9 -> This task. Proof deferred to linked slice closeout.
- request-AC10 -> This task. Proof deferred to linked slice closeout.
- request-AC11 -> This task. Proof deferred to linked slice closeout.
- request-AC12 -> This task. Proof deferred to linked slice closeout.
- request-AC13 -> This task. Proof deferred to linked slice closeout.
- request-AC14 -> This task. Proof deferred to linked slice closeout.
- request-AC15 -> This task. Proof deferred to linked slice closeout.
- request-AC16 -> This task. Proof deferred to linked slice closeout.
- request-AC17 -> This task. Proof deferred to linked slice closeout.
- request-AC18 -> This task. Proof deferred to linked slice closeout.
- request-AC19 -> This task. Proof deferred to linked slice closeout.
- request-AC20 -> This task. Proof deferred to linked slice closeout.
- request-AC21 -> This task. Proof deferred to linked slice closeout.
- request-AC22 -> This task. Proof deferred to linked slice closeout.
- request-AC25 -> This task. Proof deferred to linked slice closeout.
- request-AC24 -> This task. Proof deferred to linked slice closeout.
- request-AC23 -> This task. Proof deferred to linked slice closeout.

# Validation
- `make check` passed: compile, JSDoc type check, host self-check, i18n and hygiene.
- `make fixture` passed: four reports and defects found unaided.
- `logics-manager flow validate` passed with 0 findings; `lint --require-status` passed and `audit --group-by-doc` has no blocking issue.

# Report
- The review loop is delivered for the seven explicit CLI operations. The source pipeline is intentionally retained as the historical hardcoded chain, per `item_001`, not an unfinished conversion backlog. Task closeout remains separate because global request-AC traceability must be reconciled without inventing proof.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): (none yet)

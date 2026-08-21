## task_001_deliver_the_reviewable_operation_loop - Deliver the reviewable operation loop
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 95%
> Confidence: 90%
> Progress: 15%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-21 22:53:43

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
- [ ] 4. `item_001` -- the report writer, then the twelve operations converted to it one at a time, each checked against the numbers it printed before. Nothing else starts until this is done: every other slice reads what it writes.
- [ ] 5. `item_002` -- the runner command: the refusal to write to work/in/, operation discovery and its manifest, and the execution contract of `adr_005` (identity, parent by fingerprint, one writer per target, exit codes, heartbeat).
- [ ] 5b. `item_010` -- the two catalogues and the parity check, before the interface strings multiply. Retrofitting i18n costs more than starting with it.
- [ ] 6. `item_007` -- assert the fixture: the generated defects must be found by the sweep unaided, which is the ground truth the tools never had.
- [ ] 7. `item_003` -- the viewer: chain as a top-down DAG, report panel, image editor, menus that show commands.
- [ ] 7b. `item_012` -- the setup check: requirements, version floors, and the fix shown per platform. It comes before the first-run screen, which only renders what it produces.
- [ ] 8. `item_006` -- the first run: what to do on an empty work/ops, and the environment checks.
- [ ] 8b. `item_013` -- the bridges: evidence, resolved references, runbook scaffolding. It comes before the reverse index, which reads document titles through it.
- [ ] 9. `item_008` -- the runbook reverse index, derived from the links the reports already carry.
- [ ] 10. `item_005` -- the comparison: fixed-camera renders of both states, the wipe, the numeric difference beside it.
- [ ] 10b. `item_011` -- the platform matrix: engine discovery, the WSL path translation, and the opener. Right after the loop works on one platform, before more surface is built on top of it.
- [ ] 11. `item_009` -- STEP ingestion through FreeCAD, once the loop is proven on Blender. It is the operation that most needs the heartbeat, so it comes after it exists.
- [ ] 12. `item_004` -- pruning, only once the disk footprint is real. Not before.
- [ ] 13. Record what the loop changes about reviewing an operation as a runbook, and note in run_006 and run_009 where the reports now carry what those procedures ask to be checked by hand.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_001_define_the_operation_report_and_write_one_from_every_operation`
- `item_002_run_one_named_operation_from_a_single_agent_agnostic_command`
- `item_003_read_the_chain_of_operations_in_a_local_viewer`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

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

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_000_make_every_3d_operation_reviewable_without_reopening_blender`
- Product brief(s): `prod_001_reviewable_agent_driven_3d_operations`
- Architecture decision(s): (none yet)

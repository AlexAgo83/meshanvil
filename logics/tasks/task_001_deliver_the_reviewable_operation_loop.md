## task_001_deliver_the_reviewable_operation_loop - Deliver the reviewable operation loop
> From version: 1.0.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.

# AI Context
- Summary: Orchestrates the three slices in order: settle and write the report format, build the runner on the converted operations, then build the viewer against real reports rather than fixtures.
- Keywords: orchestration, report format, runner, viewer, conversion order
- Use when: Sequencing the work, or checking what remains before the loop is usable end to end.
- Skip when: Implementing one slice -- read its backlog item instead.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Settle the report shape against what the eight existing operations already measure, so the format records what is there rather than asking scripts to compute something new.
- [ ] 2. Implement the report writer and convert the operations to it one by one, checking each converted operation against the numbers it printed before.
- [ ] 3. Build the runner command on top of the converted operations, including the refusal to write to work/in/.
- [ ] 4. Build the viewer last, against real reports produced by the converted chain rather than fixtures.
- [ ] 5. Record what the loop changes about the way an operation is reviewed as a runbook, and note in run_006 and run_009 where the reports now carry what those procedures ask to be checked by hand.
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

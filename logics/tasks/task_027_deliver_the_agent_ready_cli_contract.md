## task_027_deliver_the_agent_ready_cli_contract - Deliver the agent-ready CLI contract
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-23 11:21:41

# AI Context
- Summary: Implementation plan for the agent-ready CLI request, ordered from schema/envelope foundations through reports, status, next advice and docs.
- Keywords: implement agent CLI, schema, status, reports, JSON envelope, next action
- Use when: delivering req_014 or coordinating its seven backlog slices.
- Skip when: scoping new AI work outside the existing CLI contract.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Add the schema command first so the rest of the JSON contract has a place to document itself.
- [ ] 2. Factor the smallest shared JSON envelope helper and move current `--json` commands onto it without changing their exit codes.
- [ ] 3. Add stable refusal codes at the CLI boundary and cover the named recovery cases without launching Blender.
- [ ] 4. Add report listing, latest-report and report-by-id commands over `work/ops`, including malformed and ambiguous cases.
- [ ] 5. Add shared status collection and expose it through `status --json`.
- [ ] 6. Add `next --json` as a pure advice command that reuses status data and never mutates project state.
- [ ] 7. Write the short agent operating contract and link it from the repository's existing docs.
- [ ] 8. Add selfchecks and pytest wrappers for each new command and envelope rule, then run `make check`, Logics lint, audit and flow validate.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_060_expose_report_operation_and_cli_schemas_from_the_tool`
- `item_061_add_one_status_json_command_for_agent_preflight`
- `item_062_let_agents_list_and_read_reports_through_the_cli`
- `item_063_standardize_json_success_and_error_envelopes`
- `item_064_give_actionable_refusals_stable_error_codes`
- `item_065_add_a_next_action_command_that_advises_without_acting`
- `item_066_document_the_agent_operating_contract`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_060_expose_report_operation_and_cli_schemas_from_the_tool`. Proof deferred to slice closeout.
- request-AC8 -> `item_060_expose_report_operation_and_cli_schemas_from_the_tool`. Proof deferred to slice closeout.
- request-AC2 -> `item_061_add_one_status_json_command_for_agent_preflight`. Proof deferred to slice closeout.
- request-AC8 -> `item_061_add_one_status_json_command_for_agent_preflight`. Proof deferred to slice closeout.
- request-AC3 -> `item_062_let_agents_list_and_read_reports_through_the_cli`. Proof deferred to slice closeout.
- request-AC8 -> `item_062_let_agents_list_and_read_reports_through_the_cli`. Proof deferred to slice closeout.
- request-AC4 -> `item_063_standardize_json_success_and_error_envelopes`. Proof deferred to slice closeout.
- request-AC8 -> `item_063_standardize_json_success_and_error_envelopes`. Proof deferred to slice closeout.
- request-AC5 -> `item_064_give_actionable_refusals_stable_error_codes`. Proof deferred to slice closeout.
- request-AC8 -> `item_064_give_actionable_refusals_stable_error_codes`. Proof deferred to slice closeout.
- request-AC6 -> `item_065_add_a_next_action_command_that_advises_without_acting`. Proof deferred to slice closeout.
- request-AC8 -> `item_065_add_a_next_action_command_that_advises_without_acting`. Proof deferred to slice closeout.
- request-AC7 -> `item_066_document_the_agent_operating_contract`. Proof deferred to slice closeout.
- request-AC8 -> `item_066_document_the_agent_operating_contract`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_014_make_the_cli_a_dependable_surface_for_ai_operators`
- Product brief(s): `prod_014_an_agent_ready_command_surface_for_meshanvil`
- Architecture decision(s): (none yet)

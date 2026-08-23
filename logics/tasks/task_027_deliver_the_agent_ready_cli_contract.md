## task_027_deliver_the_agent_ready_cli_contract - Deliver the agent-ready CLI contract
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 95%
> Confidence: 90%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-23 12:45:05
> Owner: codex

# AI Context
- Summary: Implementation plan for the agent-ready CLI request, documenting the surface first, then envelopes, error codes, reports, status and schema.
- Keywords: implement agent CLI, schema, status, reports, JSON envelope, AGENTS.md
- Use when: delivering req_014 or coordinating its six backlog slices.
- Skip when: scoping new AI work outside the existing CLI contract.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.
- The separate `next` advice command was withdrawn into the status slice, which records the supersession: `status --json` already carries the state that would produce the advice, and two commands answering the same question drift apart.

# Plan
- [x] 1. Write `AGENTS.md` against the CLI as it stands today. It ships value on its own and is the cheapest slice; revise it as the slices below land.
- [x] 2. Factor the smallest shared JSON envelope helper and move current `--json` commands onto it without changing their exit codes; fix `run --json` to return `report_path`, `id` and report `status` instead of captured stdout.
- [x] 3. Add stable refusal codes at the CLI boundary and cover the named recovery cases without launching Blender.
- [x] 4. Add report listing, latest-report and report-by-id commands over `work/ops`, including malformed and ambiguous cases.
- [x] 5. Add shared status collection and expose it through `status --json`, including the ordered next-action hints.
- [x] 6. Add `schema --json` last, once the envelope and error codes it documents are settled.
- [x] 7. Add selfchecks and pytest wrappers for each new command and envelope rule, then run `make check`, Logics lint, audit and flow validate.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_060_expose_report_operation_and_cli_schemas_from_the_tool`
- `item_061_add_one_status_json_command_for_agent_preflight`
- `item_062_let_agents_list_and_read_reports_through_the_cli`
- `item_063_standardize_json_success_and_error_envelopes`
- `item_064_give_actionable_refusals_stable_error_codes`
- `item_066_document_the_agent_operating_contract`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC8 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC2 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC8 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC3 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC8 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC4 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC8 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC5 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC8 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC6 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC6 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC7 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`
- request-AC8 -> This task. Proof: Implemented in f41a6ed; validated with make check, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract. Source: `f41a6ed`

# Validation
- (no validation recorded yet)
- make check passed on 2026-08-23: 31 tests passed; i18n ok; hygiene clean. logics-manager lint --require-status passed. logics-manager audit --group-by-doc passed with deferred warnings only. logics-manager flow validate task_027_deliver_the_agent_ready_cli_contract passed with 0 findings.
- Finish workflow executed on 2026-08-23.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-23.
- Linked backlog item(s): `item_060_expose_report_operation_and_cli_schemas_from_the_tool`, `item_061_add_one_status_json_command_for_agent_preflight`, `item_062_let_agents_list_and_read_reports_through_the_cli`, `item_063_standardize_json_success_and_error_envelopes`, `item_064_give_actionable_refusals_stable_error_codes`, `item_066_document_the_agent_operating_contract`
- Related request(s): `req_014_make_the_cli_a_dependable_surface_for_ai_operators`

# Links
- Request: `req_014_make_the_cli_a_dependable_surface_for_ai_operators`
- Product brief(s): `prod_014_an_agent_ready_command_surface_for_meshanvil`
- Architecture decision(s): (none yet)

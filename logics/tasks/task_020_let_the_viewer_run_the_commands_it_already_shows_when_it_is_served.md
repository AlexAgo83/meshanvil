## task_020_let_the_viewer_run_the_commands_it_already_shows_when_it_is_served - Let the viewer run the commands it already shows, when it is served
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: Claude
> Indicators reviewed: 2026-08-22 17:07:13

# AI Context
- Summary: Orchestrates the served-viewer execution reversal: the superseding ADR first, then the server endpoint, then the client wiring, each validated before the next, with file:// behaviour and the two out-of-scope commands confirmed unchanged at closeout.
- Keywords: orchestration, served viewer, adr supersession, closed command execution
- Use when: planning or sequencing this slice, or checking what remains before closeout.
- Skip when: the work is about a command outside the closed set, or about the plain file:// viewer.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Write the superseding ADR first: the exact boundary (localhost-only, per-launch token, one command at a time, closed command set) decided before any code depends on it.
- [ ] 2. Add the run endpoint to the existing --serve server: token check, closed command dispatch, single-flight guard, subprocess of bin/meshanvil.
- [ ] 3. Thread the per-launch token into data.js next to the other build-time payload fields.
- [ ] 4. Wire the three in-scope menu rows to the endpoint on a served page, rendering stdout/stderr/exit code; confirm file:// pages and the two out-of-scope rows are unchanged.
- [ ] 5. Extend viewer_smoke (served mode) and add a host-side check for the endpoint's token and single-flight refusal.
- [ ] 6. Mark adr_003 Superseded, cross-link it to the new ADR, and update adr_004's consequence note about the reversal cost.
- [ ] 7. Run make check, the fixture check and both smokes (file:// and --serve) before closeout.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server`
- `item_033_show_a_command_s_own_output_where_its_text_used_to_sit`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC2 -> `item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server`. Proof deferred to slice closeout.
- request-AC3 -> `item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server`. Proof deferred to slice closeout.
- request-AC4 -> `item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server`. Proof deferred to slice closeout.
- request-AC6 -> `item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server`. Proof deferred to slice closeout.
- request-AC1 -> `item_033_show_a_command_s_own_output_where_its_text_used_to_sit`. Proof deferred to slice closeout.
- request-AC5 -> `item_033_show_a_command_s_own_output_where_its_text_used_to_sit`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_006_let_the_viewer_run_the_commands_it_already_shows_when_it_is_served`
- Product brief(s): `prod_007_a_served_viewer_that_can_run_what_it_already_shows`
- Architecture decision(s): (none yet)

## task_024_deliver_the_live_viewer_and_the_module_structure - Deliver the live viewer and the module structure
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 75%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:08:22
> Owner: codex

# AI Context
- Summary: Sequences the pass: payload route first, then the event stream, then the host split, the ADR, the client split behind a committed bundle, and the test layout last.
- Keywords: orchestration, live refresh, module split, committed bundle, test layout
- Use when: Picking up or ordering the work of req_010.
- Skip when: Looking for what any one slice must satisfy -- the backlog items hold that.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 0. Capture the before-baseline this request is measured against, before touching any code: `python3 scripts/fixture_check.py` then `meshanvil view --no-open`, keeping `work/viewer/data.js` outside the tree. `work/` is gitignored, so nothing captures it for you.
- [ ] 1. Serve the payload from a route, keeping the generated file as the opened-from-disk fallback.
- [ ] 2. Make the served page what `meshanvil view` produces by default, reuse a live viewer per project, and pin its address.
- [ ] 3. Add the standard-library event stream, the component-scoped client refetch and the throttled fallback; measure the idle cost.
- [ ] 4. Split the viewer host module into payload, server and host interaction behind a route-module convention.
- [ ] 5. Record the ADR amendment: the delivered auto-refresh, the default serving mode, and the build step the client split requires.
- [ ] 6. Split the client by screen behind a committed bundle, with the staleness check and the line budget in make check.
- [ ] 7. Stand up the test layout, carry over selfcheck's assertions module by module, and extend the smoke suite over live refresh.
- [ ] 8. Re-run make check, viewer-smoke and the Logics gates before closeout, and confirm a report renders identically to before.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_045_serve_the_viewer_payload_instead_of_baking_it_into_the_page`
- `item_046_push_change_to_the_open_page_over_a_standard_library_event_stream`
- `item_047_split_the_viewer_host_module_into_payload_server_and_host_interaction`
- `item_048_split_the_client_by_screen_behind_a_committed_checked_bundle`
- `item_049_give_the_host_code_a_test_layout_with_one_module_per_host_module`, `item_050_reuse_a_running_viewer_and_keep_its_address_stable`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_045_serve_the_viewer_payload_instead_of_baking_it_into_the_page`. Proof deferred to slice closeout.
- request-AC12 -> `item_045_serve_the_viewer_payload_instead_of_baking_it_into_the_page`. Proof deferred to slice closeout.
- request-AC2 -> `item_046_push_change_to_the_open_page_over_a_standard_library_event_stream`. Proof deferred to slice closeout.
- request-AC3 -> `item_046_push_change_to_the_open_page_over_a_standard_library_event_stream`. Proof deferred to slice closeout.
- request-AC4 -> `item_046_push_change_to_the_open_page_over_a_standard_library_event_stream`. Proof deferred to slice closeout.
- request-AC5 -> `item_046_push_change_to_the_open_page_over_a_standard_library_event_stream`. Proof deferred to slice closeout.
- request-AC9 -> `item_047_split_the_viewer_host_module_into_payload_server_and_host_interaction`. Proof deferred to slice closeout.
- request-AC6 -> `item_048_split_the_client_by_screen_behind_a_committed_checked_bundle`. Proof deferred to slice closeout.
- request-AC7 -> `item_048_split_the_client_by_screen_behind_a_committed_checked_bundle`. Proof deferred to slice closeout.
- request-AC8 -> `item_048_split_the_client_by_screen_behind_a_committed_checked_bundle`. Proof deferred to slice closeout.
- request-AC10 -> `item_049_give_the_host_code_a_test_layout_with_one_module_per_host_module`, `item_050_reuse_a_running_viewer_and_keep_its_address_stable`. Proof deferred to slice closeout.
- request-AC11 -> `item_049_give_the_host_code_a_test_layout_with_one_module_per_host_module`, `item_050_reuse_a_running_viewer_and_keep_its_address_stable`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`
- Product brief(s): `prod_011_a_viewer_that_stays_current_and_a_codebase_that_stays_divisible`
- Architecture decision(s): (none yet)

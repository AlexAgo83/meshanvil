## task_024_deliver_the_live_viewer_and_the_module_structure - Deliver the live viewer and the module structure
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:27:28
> Owner: codex

# AI Context
- Summary: Sequences the pass: payload route first, then the event stream, then the host split, the ADR, the client split behind a committed bundle, and the test layout last.
- Keywords: orchestration, live refresh, module split, committed bundle, test layout
- Use when: Picking up or ordering the work of req_010.
- Skip when: Looking for what any one slice must satisfy -- the backlog items hold that.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 0. Capture the before-baseline this request is measured against, before touching any code: `python3 scripts/fixture_check.py` then `meshanvil view --no-open`, keeping `work/viewer/data.js` outside the tree. `work/` is gitignored, so nothing captures it for you.
- [x] 1. Serve the payload from a route, keeping the generated file as the opened-from-disk fallback.
- [x] 2. Make the served page what `meshanvil view` produces by default, reuse a live viewer per project, and pin its address.
- [x] 3. Add the standard-library event stream, the component-scoped client refetch and the throttled fallback; measure the idle cost.
- [x] 4. Split the viewer host module into payload, server and host interaction behind a route-module convention.
- [x] 5. Record the ADR amendment: the delivered auto-refresh, the default serving mode, and the build step the client split requires.
- [x] 6. Split the client by screen behind a committed bundle, with the staleness check and the line budget in make check.
- [x] 7. Stand up the test layout, carry over selfcheck's assertions module by module, and extend the smoke suite over live refresh.
- [x] 8. Re-run make check, viewer-smoke and the Logics gates before closeout, and confirm a report renders identically to before.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_045_serve_the_viewer_payload_instead_of_baking_it_into_the_page`
- `item_046_push_change_to_the_open_page_over_a_standard_library_event_stream`
- `item_047_split_the_viewer_host_module_into_payload_server_and_host_interaction`
- `item_048_split_the_client_by_screen_behind_a_committed_checked_bundle`
- `item_049_give_the_host_code_a_test_layout_with_one_module_per_host_module`, `item_050_reuse_a_running_viewer_and_keep_its_address_stable`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC12 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC2 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC3 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC4 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC5 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC9 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC6 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC7 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC8 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC10 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC11 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC13 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC14 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC15 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC16 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`
- request-AC17 -> This task. Proof: Implemented across 79aeead, b2a04be, 5fc5319, 63d4dc0 and cf0ddf7; validated with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure. Source: `cf0ddf7`

# Validation
- (no validation recorded yet)
- command: `make check; make viewer-smoke; logics-manager lint --require-status; logics-manager audit --group-by-doc; logics-manager flow validate task_024_deliver_the_live_viewer_and_the_module_structure` | result: passed | date: 2026-08-23
- Finish workflow executed on 2026-08-23.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-23.
- Linked backlog item(s): `item_045_serve_the_viewer_payload_instead_of_baking_it_into_the_page`, `item_046_push_change_to_the_open_page_over_a_standard_library_event_stream`, `item_047_split_the_viewer_host_module_into_payload_server_and_host_interaction`, `item_048_split_the_client_by_screen_behind_a_committed_checked_bundle`, `item_049_give_the_host_code_a_test_layout_with_one_module_per_host_module`, `item_050_reuse_a_running_viewer_and_keep_its_address_stable`
- Related request(s): `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`

# Links
- Request: `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`
- Product brief(s): `prod_011_a_viewer_that_stays_current_and_a_codebase_that_stays_divisible`
- Architecture decision(s): (none yet)

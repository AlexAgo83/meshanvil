## task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals - Deliver the viewer's direct file controls and translated result modals
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:48:56
> Owner: codex

# AI Context
- Summary: Sequences the pass: record the open/reveal rule first, build the server side against a build-owned reference set, then the icon-only file controls, the translated modals under Help, and the smoke coverage over all of it.
- Keywords: orchestration, file controls, open and reveal endpoint, translated modals, viewer smoke coverage
- Use when: Picking up or ordering the work of req_009.
- Skip when: Looking for what any one slice must satisfy -- the backlog items hold that.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 1. 1. Record the decision on how a file reaches the server without an operator-supplied path, amending adr_007 or adding an ADR.
- [x] 2. 2. Build the server side of Open and Reveal against a build-owned reference set, with its refusals.
- [x] 3. 3. Replace every file reference with the shared icon-only open/copy/reveal group, rename the label to file, and drop the blender command.
- [x] 4. 4. Give the operations list a machine-readable form and render both results as translated modals reached from Help.
- [x] 5. 5. Extend the viewer smoke suite over the new controls, the file:// degradation and both modals.
- [x] 6. 6. Re-run make check, viewer-smoke and the Logics gates before closeout.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group`
- `item_042_let_the_served_page_open_and_reveal_a_file_the_build_already_knows`
- `item_043_show_list_and_setup_results_as_translated_modals_reached_from_help`
- `item_044_cover_the_new_controls_and_modals_in_the_viewer_smoke_suite`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC2 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC4 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC6 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC3 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC5 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC7 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC8 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC9 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC10 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`
- request-AC11 -> This task. Proof: Implemented direct file controls, opaque /file open/reveal IDs, structured Help result modals, runbook command selection, smoke coverage, and focused route tests in commits 8afb37a and b509db3. Verified with make check, make viewer-smoke, logics-manager lint --require-status, logics-manager audit --group-by-doc, and flow validate task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals. Source: `b509db3`

# Validation
- (no validation recorded yet)
- command: `logics-manager audit --group-by-doc` | result: passed | date: 2026-08-23
- Finish workflow executed on 2026-08-23.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-23.
- Linked backlog item(s): `item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group`, `item_042_let_the_served_page_open_and_reveal_a_file_the_build_already_knows`, `item_043_show_list_and_setup_results_as_translated_modals_reached_from_help`, `item_044_cover_the_new_controls_and_modals_in_the_viewer_smoke_suite`
- Related request(s): `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls`

# Links
- Request: `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls`
- Product brief(s): `prod_010_direct_controls_over_the_files_and_results_the_viewer_already_names`
- Architecture decision(s): (none yet)

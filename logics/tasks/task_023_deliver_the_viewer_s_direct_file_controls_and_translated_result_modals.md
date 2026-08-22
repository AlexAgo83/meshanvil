## task_023_deliver_the_viewer_s_direct_file_controls_and_translated_result_modals - Deliver the viewer's direct file controls and translated result modals
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:18:46

# AI Context
- Summary: Sequences the pass: record the open/reveal rule first, build the server side against a build-owned reference set, then the icon-only file controls, the translated modals under Help, and the smoke coverage over all of it.
- Keywords: orchestration, file controls, open and reveal endpoint, translated modals, viewer smoke coverage
- Use when: Picking up or ordering the work of req_009.
- Skip when: Looking for what any one slice must satisfy -- the backlog items hold that.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. 1. Record the decision on how a file reaches the server without an operator-supplied path, amending adr_007 or adding an ADR.
- [ ] 2. 2. Build the server side of Open and Reveal against a build-owned reference set, with its refusals.
- [ ] 3. 3. Replace every file reference with the shared icon-only open/copy/reveal group, rename the label to file, and drop the blender command.
- [ ] 4. 4. Give the operations list a machine-readable form and render both results as translated modals reached from Help.
- [ ] 5. 5. Extend the viewer smoke suite over the new controls, the file:// degradation and both modals.
- [ ] 6. 6. Re-run make check, viewer-smoke and the Logics gates before closeout.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group`
- `item_042_let_the_served_page_open_and_reveal_a_file_the_build_already_knows`
- `item_043_show_list_and_setup_results_as_translated_modals_reached_from_help`
- `item_044_cover_the_new_controls_and_modals_in_the_viewer_smoke_suite`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group`. Proof deferred to slice closeout.
- request-AC2 -> `item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group`. Proof deferred to slice closeout.
- request-AC4 -> `item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group`. Proof deferred to slice closeout.
- request-AC6 -> `item_041_replace_each_file_reference_with_an_icon_only_open_copy_and_reveal_group`. Proof deferred to slice closeout.
- request-AC3 -> `item_042_let_the_served_page_open_and_reveal_a_file_the_build_already_knows`. Proof deferred to slice closeout.
- request-AC5 -> `item_042_let_the_served_page_open_and_reveal_a_file_the_build_already_knows`. Proof deferred to slice closeout.
- request-AC7 -> `item_043_show_list_and_setup_results_as_translated_modals_reached_from_help`. Proof deferred to slice closeout.
- request-AC8 -> `item_043_show_list_and_setup_results_as_translated_modals_reached_from_help`. Proof deferred to slice closeout.
- request-AC9 -> `item_043_show_list_and_setup_results_as_translated_modals_reached_from_help`. Proof deferred to slice closeout.
- request-AC10 -> `item_044_cover_the_new_controls_and_modals_in_the_viewer_smoke_suite`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls`
- Product brief(s): `prod_010_direct_controls_over_the_files_and_results_the_viewer_already_names`
- Architecture decision(s): (none yet)

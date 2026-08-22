## task_016_deliver_remaining_viewer_mockup_parity_gaps - Deliver remaining viewer mockup parity gaps
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-22 02:21:09
> Owner: codex

# AI Context
- Summary: Orchestrates the strict second viewer parity pass for the specific mockup surfaces missed after req_001.
- Keywords: deliver, remaining, viewer, mockup, parity, gaps
- Use when: Planning, implementing, validating or closing the menu, Runbooks, splash, Compare and smoke-test parity work.
- Skip when: Work belongs to engine operations, schema migration or unrelated Logics workflow maintenance.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Diff the mockup selectors against the current viewer and keep the required surface checklist in the task notes.
- [ ] 2. Implement command menus with the existing static page patterns.
- [ ] 3. Implement the Runbooks workspace as the primary center surface for that tab.
- [ ] 4. Implement the splash surface and Compare split layout without adding dependencies.
- [ ] 5. Extend the browser smoke to assert menus, Runbooks, splash and Compare.
- [ ] 6. Run make check, browser smoke and Logics validation before closeout.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_017_replace_minimal_menus_with_the_reviewed_command_menu_surface`
- `item_018_build_runbooks_as_a_primary_workspace_instead_of_an_outliner_only_list`
- `item_019_restore_the_reviewed_first_run_splash_and_compare_split_layout`
- `item_020_make_browser_smoke_fail_on_missing_mockup_surfaces`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_017_replace_minimal_menus_with_the_reviewed_command_menu_surface`. Proof deferred to slice closeout.
- request-AC6 -> `item_017_replace_minimal_menus_with_the_reviewed_command_menu_surface`. Proof deferred to slice closeout.
- request-AC2 -> `item_018_build_runbooks_as_a_primary_workspace_instead_of_an_outliner_only_list`. Proof deferred to slice closeout.
- request-AC6 -> `item_018_build_runbooks_as_a_primary_workspace_instead_of_an_outliner_only_list`. Proof deferred to slice closeout.
- request-AC3 -> `item_019_restore_the_reviewed_first_run_splash_and_compare_split_layout`. Proof deferred to slice closeout.
- request-AC4 -> `item_019_restore_the_reviewed_first_run_splash_and_compare_split_layout`. Proof deferred to slice closeout.
- request-AC6 -> `item_019_restore_the_reviewed_first_run_splash_and_compare_split_layout`. Proof deferred to slice closeout.
- request-AC5 -> `item_020_make_browser_smoke_fail_on_missing_mockup_surfaces`. Proof deferred to slice closeout.
- request-AC6 -> `item_020_make_browser_smoke_fail_on_missing_mockup_surfaces`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_002_close_the_remaining_local_viewer_mockup_parity_gaps`
- Product brief(s): `prod_003_strict_local_viewer_mockup_parity_closure`
- Architecture decision(s): (none yet)

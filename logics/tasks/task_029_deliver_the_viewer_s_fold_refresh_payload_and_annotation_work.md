## task_029_deliver_the_viewer_s_fold_refresh_payload_and_annotation_work - Deliver the viewer's fold, refresh, payload and annotation work
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 50%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-25 00:23:17
> Owner: claude

# AI Context
- Summary: Four viewer items whose order matters: the fold is a shipped defect and the cheapest, the refresh hides a bug that must be separated from its tuning, the annotations constrain nothing else, and the payload touches the file:// snapshot every other screen depends on. The fold, the refresh and the payload all read the same DATA object, which is why two of the three defects come from replacing it too bluntly.
- Keywords: viewer delivery order, fold defect, refresh bug versus tuning, annotation storage, payload last, browser smoke, DOM-free rules
- Use when: Picking up any of the four viewer items, or deciding which to start with.
- Skip when: The work is a single isolated viewer fix with no bearing on the DATA object or the payload.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Read viewer/src/app.js, chains.js and live.js together before changing any of them: the fold, the refresh and the payload all read the same DATA object, and two of the three defects come from how bluntly it is replaced.
- [ ] 2. Fold first. It is the smallest, it is a defect in shipped behaviour, and its check belongs in the browser smoke where the orphaned branches are visible.
- [ ] 3. Then the refresh. Fix the selection being replaced before touching the cadence: the two are independent, and only the first is a bug.
- [ ] 4. Then the annotations, because their storage decision constrains nothing else and unblocks the operator work that motivated the request.
- [ ] 5. The payload last: it is the only item whose cost is measured rather than felt, and it touches the file:// snapshot, which every other screen depends on.
- [ ] 6. Prove each behaviour where it can be proved: pure rules in viewer/src checked without a DOM, rendered results in scripts/viewer_smoke.py, server routes in scripts/selfcheck.py. Verify each new check fails when its behaviour is reverted, as the existing ones were.
- [ ] 7. Run make check and make viewer-smoke after each item rather than at the end, and re-run the demonstration chains if anything in the payload or the routes changes.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_071_fold_a_chain_and_everything_under_it_from_one_visible_control`
- `item_072_keep_the_operator_s_choices_across_a_live_refresh`
- `item_073_fetch_what_the_first_paint_draws_and_the_rest_when_it_is_needed`
- `item_074_let_a_human_say_what_the_numbers_do_not_without_touching_the_reports`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_071_fold_a_chain_and_everything_under_it_from_one_visible_control`. Proof deferred to slice closeout.
- request-AC2 -> `item_071_fold_a_chain_and_everything_under_it_from_one_visible_control`. Proof deferred to slice closeout.
- request-AC3 -> `item_071_fold_a_chain_and_everything_under_it_from_one_visible_control`. Proof deferred to slice closeout.
- request-AC9 -> `item_071_fold_a_chain_and_everything_under_it_from_one_visible_control`. Proof deferred to slice closeout.
- request-AC4 -> `item_072_keep_the_operator_s_choices_across_a_live_refresh`. Proof deferred to slice closeout.
- request-AC5 -> `item_072_keep_the_operator_s_choices_across_a_live_refresh`. Proof deferred to slice closeout.
- request-AC9 -> `item_072_keep_the_operator_s_choices_across_a_live_refresh`. Proof deferred to slice closeout.
- request-AC6 -> `item_073_fetch_what_the_first_paint_draws_and_the_rest_when_it_is_needed`. Proof deferred to slice closeout.
- request-AC9 -> `item_073_fetch_what_the_first_paint_draws_and_the_rest_when_it_is_needed`. Proof deferred to slice closeout.
- request-AC7 -> `item_074_let_a_human_say_what_the_numbers_do_not_without_touching_the_reports`. Proof deferred to slice closeout.
- request-AC8 -> `item_074_let_a_human_say_what_the_numbers_do_not_without_touching_the_reports`. Proof deferred to slice closeout.
- request-AC9 -> `item_074_let_a_human_say_what_the_numbers_do_not_without_touching_the_reports`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_016_make_the_viewer_s_outliner_refresh_and_annotations_hold_up_in_daily_use`
- Product brief(s): `prod_015_a_viewer_that_keeps_up_with_the_work`
- Architecture decision(s): (none yet)

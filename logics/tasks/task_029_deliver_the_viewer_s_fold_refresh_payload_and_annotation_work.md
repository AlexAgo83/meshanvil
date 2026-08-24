## task_029_deliver_the_viewer_s_fold_refresh_payload_and_annotation_work - Deliver the viewer's fold, refresh, payload and annotation work
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-25 01:11:21
> Owner: claude

# AI Context
- Summary: Four viewer items whose order matters: the fold is a shipped defect and the cheapest, the refresh hides a bug that must be separated from its tuning, the annotations constrain nothing else, and the payload touches the file:// snapshot every other screen depends on. The fold, the refresh and the payload all read the same DATA object, which is why two of the three defects come from replacing it too bluntly.
- Keywords: viewer delivery order, fold defect, refresh bug versus tuning, annotation storage, payload last, browser smoke, DOM-free rules
- Use when: Picking up any of the four viewer items, or deciding which to start with.
- Skip when: The work is a single isolated viewer fix with no bearing on the DATA object or the payload.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 1. Read viewer/src/app.js, chains.js and live.js together before changing any of them: the fold, the refresh and the payload all read the same DATA object, and two of the three defects come from how bluntly it is replaced.
- [x] 2. Fold first. It is the smallest, it is a defect in shipped behaviour, and its check belongs in the browser smoke where the orphaned branches are visible.
- [x] 3. Then the refresh. Fix the selection being replaced before touching the cadence: the two are independent, and only the first is a bug.
- [x] 4. Then the annotations, because their storage decision constrains nothing else and unblocks the operator work that motivated the request.
- [x] 5. The payload last: it is the only item whose cost is measured rather than felt, and it touches the file:// snapshot, which every other screen depends on.
- [x] 6. Prove each behaviour where it can be proved: pure rules in viewer/src checked without a DOM, rendered results in scripts/viewer_smoke.py, server routes in scripts/selfcheck.py. Verify each new check fails when its behaviour is reverted, as the existing ones were.
- [x] 7. Run make check and make viewer-smoke after each item rather than at the end, and re-run the demonstration chains if anything in the payload or the routes changes.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_071_fold_a_chain_and_everything_under_it_from_one_visible_control`
- `item_072_keep_the_operator_s_choices_across_a_live_refresh`
- `item_073_fetch_what_the_first_paint_draws_and_the_rest_when_it_is_needed`
- `item_074_let_a_human_say_what_the_numbers_do_not_without_touching_the_reports`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented in `48d2963`; folding is keyed on the chain, so a chain's branches go with it, headers included. `scripts/viewer_smoke.py` fails if a folded chain keeps a branch header, verified against the old group keying.
- request-AC2 -> This task. Proof: Implemented in `48d2963`; a branch header is a heading again with no fold control, and the smoke asserts no fold button is a branch.
- request-AC3 -> This task. Proof: Implemented in `48d2963`; the control is a bordered box brighter than the per-row triangles, brightens on hover, and `aria-expanded` is asserted against the glyph in both states.
- request-AC4 -> This task. Proof: Implemented in `59bf3b7`; `fetchData` carries the chosen project across the assignment. The served smoke selects another project, refreshes, and fails if the selection or the fold state moved.
- request-AC5 -> This task. Proof: Implemented in `59bf3b7`; the events route sleeps a declared `INTERVAL` minus the scan's duration. `tests/test_viewer.py::test_events_cadence_is_declared` makes the scan ten times dearer and asserts the period holds; verified against the old backoff.
- request-AC6 -> This task. Proof: Implemented in `8e9275a`; the served first paint is 268 KB against 623 KB, with two guarded read-only routes for the rest. `test_first_paint_carries_what_it_draws` asserts both payload shapes come from one builder.
- request-AC7 -> This task. Proof: Implemented in `b44e1e4` and `f3c2a68`; the served smoke types a note, refreshes, finds it and clears it, and names a chain without hiding the file it starts from.
- request-AC8 -> This task. Proof: Implemented in `b44e1e4`; `test_annotations_stay_out_of_the_reports` asserts a report's bytes are unchanged by every write path and that an interrupted rename leaves the previous file with no temporary behind.
- request-AC9 -> This task. Proof: Implemented across the five commits above; pure rules checked without a DOM in `viewer/src`, rendered results in `scripts/viewer_smoke.py`, routes in `scripts/selfcheck.py`, each verified to fail when reverted.
- request-AC10 -> This task. Proof: Recorded in `adr_009_let_the_served_viewer_write_annotations_and_nothing_else` before the route existed; six malformed or unauthorised requests are asserted refused.
# Validation
- (no validation recorded yet)
- make check passed on 2026-08-25: 35 checks, types ok, viewer bundle ok, viewer-test ok, i18n 260 keys 2 languages, hygiene clean
- make viewer-smoke passed on 2026-08-25: browser smoke ok; every new assertion verified to fail when its behaviour is reverted
- command: `make check && make viewer-smoke` | result: passed | date: 2026-08-25
- Finish workflow executed on 2026-08-25.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-25.
- Linked backlog item(s): `item_071_fold_a_chain_and_everything_under_it_from_one_visible_control`, `item_072_keep_the_operator_s_choices_across_a_live_refresh`, `item_073_fetch_what_the_first_paint_draws_and_the_rest_when_it_is_needed`, `item_074_let_a_human_say_what_the_numbers_do_not_without_touching_the_reports`
- Related request(s): `req_016_make_the_viewer_s_outliner_refresh_and_annotations_hold_up_in_daily_use`

# Links
- Request: `req_016_make_the_viewer_s_outliner_refresh_and_annotations_hold_up_in_daily_use`
- Product brief(s): `prod_015_a_viewer_that_keeps_up_with_the_work`
- Architecture decision(s): (none yet)

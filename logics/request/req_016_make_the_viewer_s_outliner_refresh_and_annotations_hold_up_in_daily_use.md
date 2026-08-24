## req_016_make_the_viewer_s_outliner_refresh_and_annotations_hold_up_in_daily_use - Make the viewer's outliner, refresh and annotations hold up in daily use
> From version: 0.1.0
> Schema version: 1.0
> Status: Draft
> Understanding: 90%
> Confidence: 85%
> Complexity: High
> Theme: Viewer usability and live state
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-25 00:04:57

# AI Context
- Summary: Four defects that only appear once a project has several chains and several sibling projects: folding a chain orphans its branches, a background refresh silently undoes the operator's project choice, the live channel's cadence is derived from its own scan cost so it slows as the project grows, and the first paint ships every project's reports and every runbook's body. Plus the one thing the page cannot hold at all -- what a person knows about a report that its numbers do not say.
- Keywords: outliner fold, chain and branch, live refresh, DATA.active, events cadence, first paint payload, lazy fetch, report note, chain name, annotations outside reports
- Use when: Changing anything in viewer/src that reads or replaces the DATA object, touching the events route's timing, deciding where operator-written content is stored, or adding a control to the outliner.
- Skip when: The work is about what an operation records or how a report is shaped -- the report schema is explicitly out of scope here, and annotations exist precisely so that reports stay the engine's own record.

# Needs
- Group folding was added per group rather than per chain. Folding a chain leaves its branches on screen with nothing above them, which reads worse than not folding at all, and every branch row carries a fold control that folds a group nobody thinks of as foldable.
- The fold affordance reuses the dim used by the per-row triangles. It is a control and reads as decoration, so operators do not discover it.
- A live refresh replaces the whole DATA object, `active` included, so an operator who has switched projects is silently returned to the served one the next time anything on disk changes. This is a defect, not a tuning question: the project selector reads data already in memory and would otherwise be instant.
- The events channel sleeps `max(1s, scan_cost * 20)`. Its cadence is therefore a function of how expensive its own scan is, which grows with the number of projects and reports -- the viewer becomes less responsive the more it is used.
- Every refresh refetches the whole payload and repaints the page, whatever changed.
- The first paint ships everything: measured at 623 KB, of which 217 KB is the reports of all sibling projects (the active one duplicated) and 124 KB is the full text of every runbook, none of it needed until something is clicked.
- There is nowhere to write down why a report matters. An operator returning to a chain, or an agent picking it up later, has the numbers and none of the reasoning -- which parameter was a guess, which finding was already investigated, what the next attempt should change.
- A chain is identified by its source file name. Two chains from similar files are told apart by reading paths, and a chain cannot be given the name the work actually has.

# Context
- The viewer is a static page over reports written by operations; adr_001 and adr_003 set the boundary that the page reads and does not establish. Annotations are the first content the page would let a human write, so where they live matters more than how they render.
- Reports are the record of what an engine did, and the project's premise is that every number in them came out of Blender. Mixing human prose into them would dilute exactly what makes them evidence.
- The served page and the file:// snapshot share one built page. Anything added to the payload or the markup has to work in both, or be added only to the served response.
- The rules that decide grouping already live in viewer/src/chains.js so they can be checked without a DOM; scripts/viewer_smoke.py covers what only a browser can prove.

# Acceptance criteria
- AC1: Folding a chain in the outliner hides that chain's rows and the rows of every branch below it, and unfolding restores exactly what was hidden.
- AC2: Only a chain header carries a fold control. A branch header carries none, because folding a branch independently is no longer possible.
- AC3: The fold control is legible without hovering: it is visually distinct from the per-row triangles it sits above, and its state is readable at a glance and through aria-expanded.
- AC4: A live refresh preserves the operator's project selection, the selected report, and the fold state.
- AC5: The cadence of the events channel is bounded by a declared interval rather than derived from its own scan cost, so a project with eight sibling projects is no less responsive than one with a single project.
- AC6: The first paint fetches only what it draws. Runbook bodies and the reports of projects other than the active one are fetched when they are first needed, and the page renders a placeholder in the meantime rather than an empty region.
- AC7: An operator can write and edit a free-text note on any report, and a name on any chain, from the page; both survive a live refresh, a page reload and a server restart.
- AC8: Annotations are stored outside the reports, in one flat JSON file readable with `cat`, keyed so that a note follows its report and a chain name follows the sha256 of the source file rather than its path.
- AC9: Every behaviour above is covered where it can be proved: the grouping and annotation rules without a DOM in viewer/src, the rendered result in the browser smoke, and the server routes in the Python checks.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_015_a_viewer_that_keeps_up_with_the_work`
- Architecture decision(s): (none yet)

# References
- viewer/src/app.js
- viewer/src/chains.js
- viewer/src/chains.test.js
- viewer/src/live.js
- viewer/viewer.css
- viewer/index.html
- meshanvil/viewer_routes/events.py
- meshanvil/viewer_payload.py
- meshanvil/viewer_server.py
- meshanvil/viewer_routes
- scripts/viewer_smoke.py
- scripts/selfcheck.py
- tests/test_viewer.py
- locales/en.json
- locales/fr.json
- work/viewer/data.js

# Backlog
- `item_071_fold_a_chain_and_everything_under_it_from_one_visible_control`
- `item_072_keep_the_operator_s_choices_across_a_live_refresh`
- `item_073_fetch_what_the_first_paint_draws_and_the_rest_when_it_is_needed`
- `item_074_let_a_human_say_what_the_numbers_do_not_without_touching_the_reports`

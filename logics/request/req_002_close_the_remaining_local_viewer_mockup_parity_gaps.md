## req_002_close_the_remaining_local_viewer_mockup_parity_gaps - Close the remaining local viewer mockup parity gaps
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 02:29:57

# AI Context
- Summary: Follow-up viewer parity request for the mockup blocks missed by the first pass: command menus, Runbooks, splash and Compare.
- Keywords: close, remaining, local, viewer, mockup, parity, gaps
- Use when: Work concerns visible local viewer parity against `logics/external/viewer-mockup.html`.
- Skip when: Work concerns operation execution, report schema changes or non-viewer engine behavior.

# Needs
- The previous viewer parity pass made the page usable but did not lock down all visible surfaces from the reviewed mockup.
- Operators must see the same major interaction areas as the mockup: command menus, a real Runbooks workspace, first-run splash guidance and the comparison split surface.
- The browser smoke test must assert those surfaces directly so future parity claims fail when a major mockup block is missing.

# Context
- The existing viewer remains a local, read-only HTML/CSS/JavaScript page over generated report data.
- The reviewed mockup is the source of truth for the required menu, runbook, splash and compare structures.
- This is a follow-up to the closed viewer parity request; the gap is specification coverage, not engine behavior.

# Acceptance criteria
- AC1: The top bar exposes mockup-style command menus with grouped rows, separators, shortcuts or hints, and selectable CLI text; the menus never execute commands, fetch data or write files.
- AC2: Selecting Runbooks replaces the central review area with a primary runbook coverage surface matching the mockup structure; rows show title, purpose, status and applied-operation chips, with unapplied runbooks visible.
- AC3: Start opens the reviewed first-run splash surface with template command cards, recent-chain empty state, environment or doctor checks, fix commands and close or primary actions; no panel is blank.
- AC4: Compare uses the mockup split layout with visible handle, before/after labels and metadata while preserving pointer drag and keyboard adjustment through a native control.
- AC5: A real-browser smoke check opens the fixture page, exercises command menus, Runbooks, splash and Compare, and fails when required mockup selectors or states are absent; screenshots remain outside the repository.
- AC6: The viewer keeps its safety boundary: no build step, no server, no engine execution, no privileged browser API, escaped report data and updated i18n strings for all new visible labels.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_003_strict_local_viewer_mockup_parity_closure`
- Architecture decision(s): (none yet)

# References
- logics/external/viewer-mockup.html
- viewer/index.html
- viewer/viewer.js
- viewer/viewer.css
- scripts/viewer_smoke.py

# Backlog
- `item_017_replace_minimal_menus_with_the_reviewed_command_menu_surface`
- `item_018_build_runbooks_as_a_primary_workspace_instead_of_an_outliner_only_list`
- `item_019_restore_the_reviewed_first_run_splash_and_compare_split_layout`
- `item_020_make_browser_smoke_fail_on_missing_mockup_surfaces`

# AC Traceability
- request-AC1 -> This task. Proof: Implemented in `4f93979`; grouped command menus expose rows, separators, shortcuts and selectable CLI text, and `scripts/viewer_smoke.py` asserts the command menu surface.
- request-AC2 -> This task. Proof: Implemented in `4f93979`; Runbooks renders a central `rbbody`/`rbrow` workspace from existing runbook data, and `scripts/viewer_smoke.py` asserts runbook rows, purpose text and applied-operation cells.
- request-AC3 -> This task. Proof: Implemented in `4f93979` and refined in `a9f36b2`; Start opens a splash with templates, explicit demo dataset command, recent-chain state, checks, fix guidance and close/primary actions, asserted by `scripts/viewer_smoke.py`.
- request-AC4 -> This task. Proof: Implemented in `4f93979`; Compare renders a wipe/split layout with labels, handle, metadata and the existing native range control, asserted by `scripts/viewer_smoke.py`.
- request-AC5 -> This task. Proof: Implemented in `4f93979` and `a9f36b2`; `scripts/viewer_smoke.py` exercises menus, Runbooks, splash, demo dataset option and Compare, writing screenshots to the system temporary directory.
- request-AC6 -> This task. Proof: Validated in `9f87609` and after `a9f36b2` with `make check` and `python3 scripts/viewer_smoke.py`; the viewer remains static/read-only, i18n passes, and no fetch or execution path was added.

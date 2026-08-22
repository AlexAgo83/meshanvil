## req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface - Bring the local viewer up to the reviewed mockup interaction surface
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: Medium
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:26:23
> Owner: codex

# AI Context
- Summary: Restore the reviewed viewer navigation, comparison and discovery surfaces while keeping the browser strictly read-only.
- Keywords: bring, local, viewer, reviewed, mockup, interaction, surface
- Use when: Changing viewer interaction, first-run guidance or browser-level verification.
- Skip when: Changing report schema, engine operations or the command runner.

# Needs
- The local viewer must retain the interaction surfaces agreed in the reviewed mockup, not merely its visual theme.
- An operator must be able to find a report, compare its states, read linked runbooks and discover commands without the viewer ever executing one.
- Viewer regressions need a real-browser check over generated fixture reports; static source assertions alone cannot prove interaction or layout.

# Context
- The current viewer already renders the report DAG, detail panel, runbook links, first-run guidance and an in-place image wipe.
- The mockup additionally specifies command menus, Chain/Compare/Runbooks workspaces, an outliner filter, a report-section rail, a labelled comparison handle and a richer first-run splash.
- The viewer remains a plain local page: it reads report files, has no framework or build requirement, and must never start an operation.

# Acceptance criteria
- AC1: The viewer exposes Chain, Compare and Runbooks workspaces; each is keyboard-accessible and preserves the selected report where applicable.
- AC2: Menus and visible actions show copyable CLI commands but never execute an operation, open an engine or mutate work/.
- AC3: The outliner filters operation and runbook rows by visible text without changing the underlying report chain.
- AC4: The comparison view labels both states, exposes a visible divider, and supports pointer drag plus keyboard range adjustment through a native control.
- AC5: First run presents the available starter commands, recent-chain absence, doctor results and platform-specific fixes without any blank panel.
- AC6: A repeatable Chrome smoke test opens the generated fixture, exercises workspace, filter and wipe interactions, and captures screenshots outside the repository.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_002_reviewable_local_viewer_interaction_parity`
- Architecture decision(s): (none yet)

# References
- logics/external/viewer-mockup.html
- viewer/index.html
- viewer/viewer.js
- viewer/viewer.css
- scripts/selfcheck.py

# Backlog
- `item_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer`
- `item_015_complete_the_mockup_review_controls_without_weakening_the_local_page_boundary`
- `item_016_exercise_the_viewer_in_a_real_browser_against_the_generated_fixture`

## task_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer - Add safe workspace navigation and command discovery to the viewer
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 95%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:34:03
> Owner: codex

# AI Context
- Summary: Deliver keyboard-accessible Chain, Compare and Runbooks navigation plus CLI-only command discovery.
- Keywords: add, safe, workspace, navigation, command, discovery, viewer
- Use when: Changing top-level viewer navigation or action discovery.
- Skip when: Adding filters, detailed comparison controls or browser smoke coverage.

# Definition of Done (DoD)
- [x] The backlog scope is implemented.
- [x] Acceptance criteria are covered.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# Backlog
- `item_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer`

# Acceptance criteria
- AC1: Each workspace can be selected by mouse and keyboard and reports remain readable after changing workspace.
- AC2: Every menu action displays its CLI command and no action invokes fetch, a process, or a write operation.

# Plan
- [ ] Use `python3 -m logics_manager flow progress task task_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer.md --progress <n>%` during multi-wave work.
- [ ] Run `python3 -m logics_manager flow finish task task_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer.md` after implementation.

# Validation
- (no validation recorded yet)
- Finish workflow executed on 2026-08-22.
- Linked backlog/request close verification passed.

# Report
- Delivered in `55261b0`: native workspace tabs and command-only menus. AC evidence is recorded below. `flow finish` remains structurally blocked while the orchestration task is also linked to this backlog item.
- Finished on 2026-08-22.
- Linked backlog item(s): `item_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer`
- Related request(s): `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`

# Links
- Request: `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

# Evidence
- AC1 | date: 2026-08-22 | command: `make check; meshanvil view --no-open; Google Chrome --headless` | result: passed | Native tab buttons retain the selected report while switching Chain, Compare and Runbooks; Compare expands the existing image editor.
- AC2 | date: 2026-08-22 | command: `make check` | result: passed | Native details menus expose selectable CLI commands only; the runnable self-check rejects any fetch call in viewer.js.

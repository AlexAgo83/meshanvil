## task_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer - Add safe workspace navigation and command discovery to the viewer
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:30:20
> Owner: codex

# AI Context
- Summary: Deliver keyboard-accessible Chain, Compare and Runbooks navigation plus CLI-only command discovery.
- Keywords: add, safe, workspace, navigation, command, discovery, viewer
- Use when: Changing top-level viewer navigation or action discovery.
- Skip when: Adding filters, detailed comparison controls or browser smoke coverage.

# Definition of Done (DoD)
- [ ] The backlog scope is implemented.
- [ ] Acceptance criteria are covered.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

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

# Report
- Not started.

# Links
- Request: `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

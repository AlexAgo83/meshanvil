## item_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer - Add safe workspace navigation and command discovery to the viewer
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 45%
> Complexity: Medium
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 01:26:05

# AI Context
- Summary: Make Chain, Compare and Runbooks explicit workspaces and expose CLI guidance without browser-side execution.
- Keywords: add, safe, workspace, navigation, command, discovery, viewer
- Use when: Implementing tabs, command menus or selection handoff between viewer workspaces.
- Skip when: Adding filter controls, changing the wipe, or testing browser interaction.

# Problem
- The current page implements the Chain surface only, although the reviewed mockup makes comparison and runbooks first-class workspaces.
- The current page has no menus that teach the CLI commands available to the operator.

# Scope
- In:
  - Chain, Compare and Runbooks tabs using the current static page and report payload.
  - Accessible menus that reveal commands as text and use no execution endpoint or browser-side mutation.
  - Selection and focus behavior shared by the three workspaces.
- Out:
  - Running commands, clipboard permissions, opening Blender, or adding a server API.
  - Replacing the report-driven graph or details panel.

# Acceptance criteria
- AC1: Each workspace can be selected by mouse and keyboard and reports remain readable after changing workspace.
- AC2: Every menu action displays its CLI command and no action invokes fetch, a process, or a write operation.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Each workspace can be selected by mouse and keyboard and reports remain readable after changing workspace.
- request-AC2 -> This backlog slice. Proof: AC2: Every menu action displays its CLI command and no action invokes fetch, a process, or a write operation.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_002_reviewable_local_viewer_interaction_parity`
- Architecture decision(s): (none yet)
- Request: `req_001_bring_the_local_viewer_up_to_the_reviewed_mockup_interaction_surface`
- Primary task(s): `task_012_deliver_reviewed_viewer_interaction_parity`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_014_add_safe_workspace_navigation_and_command_discovery_to_the_viewer`

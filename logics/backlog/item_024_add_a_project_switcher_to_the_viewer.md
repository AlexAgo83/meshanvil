## item_024_add_a_project_switcher_to_the_viewer - Add a project switcher to the viewer
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 40%
> Complexity: Medium
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 14:34:51

# AI Context
- Summary: The page is built for one report directory and names a fixed path. It has to list the projects that hold reports, let the operator select one, and scope every count and total to the one shown -- without a rebuild, a request or a write.
- Keywords: viewer switcher, project selection, read-only page, top bar, status bar, totals scoping
- Use when: changing what the viewer shows about a project, or any surface that currently names a fixed path.
- Skip when: the change concerns a single report's contents rather than which project is displayed.
# Problem
- The viewer is built for one report directory and has no way to reach another.
- The top bar names a fixed path rather than the project, and the status bar totals describe whatever the directory happens to hold.
- Switching today means rebuilding the page and opening it again by hand.

# Scope
- In:
  - Generate the page with the projects that hold reports and let the operator select one from the page.
  - Show the active project where the fixed path is shown today, in the top bar and the status bar.
  - Keep counts, branch totals and vertex totals scoped to the shown project.
- Out:
  - Drawing two projects in one graph, or comparing operations across projects.
  - Any fetch, server, build step or write from the page.
  - Persisting the selection outside the viewer.

# Acceptance criteria
- AC1: The page lists the projects that hold at least one report and marks which one is shown.
- AC2: Selecting a project shows its chain, outliner groups, renders and totals without a rebuild and without a network request.
- AC3: The top bar and status bar name the shown project instead of a fixed path.
- AC4: With a single project the page reads as it does today, with no empty switcher furniture.
- AC5: New visible labels are present in the i18n catalogue and report data stays escaped.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: The page lists the projects that hold at least one report and marks which one is shown.
- request-AC5 -> This backlog slice. Proof: AC2: Selecting a project shows its chain, outliner groups, renders and totals without a rebuild and without a network request.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_004_multi_project_operator_workspaces`
- Architecture decision(s): (none yet)
- Request: `req_003_hold_several_model_projects_side_by_side_and_switch_between_them`
- Primary task(s): `task_017_deliver_multi_project_workspaces_and_the_viewer_switcher`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

## item_018_build_runbooks_as_a_primary_workspace_instead_of_an_outliner_only_list - Build Runbooks as a primary workspace instead of an outliner-only list
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 85%
> Complexity: Medium
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 02:21:09

# AI Context
- Summary: Make Runbooks a central workspace with coverage rows and applied-operation chips, not only an outliner/detail side feature.
- Keywords: build, runbooks, primary, workspace, instead, outliner, only, list
- Use when: Implementing or testing the Runbooks tab, runbook rows, applied chips or unapplied states.
- Skip when: Work is about executing runbooks or changing workflow document lifecycle.

# Problem
- Runbooks currently appear mainly as outliner entries and detail-panel metadata.
- The mockup shows a dedicated Runbooks screen with coverage rows and applied-operation relationships.

# Scope
- In:
  - Switching to Runbooks replaces the central review area with a runbook coverage body.
  - Rows show title, purpose, status and applied-operation chips using existing report and runbook data.
  - Unapplied or unavailable runbooks have explicit visible states.
- Out:
  - Executing runbook commands from the browser.
  - Persisted workflow state, external document fetching or schema changes.

# Acceptance criteria
- AC1: The Runbooks workspace has a central list or table with one row per available runbook.
- AC2: Applied operation chips are visible and selecting them focuses the linked report when data exists.
- AC3: Unapplied runbooks remain visible with an explicit unapplied state instead of disappearing.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: The Runbooks workspace has a central list or table with one row per available runbook.
- request-AC6 -> This backlog slice. Proof: AC2: Applied operation chips are visible and selecting them focuses the linked report when data exists.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_003_strict_local_viewer_mockup_parity_closure`
- Architecture decision(s): (none yet)
- Request: `req_002_close_the_remaining_local_viewer_mockup_parity_gaps`
- Primary task(s): `task_016_deliver_remaining_viewer_mockup_parity_gaps`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

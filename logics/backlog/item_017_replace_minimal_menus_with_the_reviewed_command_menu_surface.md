## item_017_replace_minimal_menus_with_the_reviewed_command_menu_surface - Replace minimal menus with the reviewed command menu surface
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Low
> Theme: Viewer parity
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 02:21:09

# AI Context
- Summary: Replace the current small native menu content with the reviewed grouped command-menu surface while staying read-only.
- Keywords: replace, minimal, menus, reviewed, command, menu, surface
- Use when: Implementing or testing top-bar command menu structure, labels, shortcuts and safe command text.
- Skip when: Work is about executing commands, clipboard permissions or non-menu viewer layout.

# Problem
- The current viewer uses minimal native details menus and only a few command rows.
- The mockup expects richer grouped command menus with shortcuts, separators and command-style rows.

# Scope
- In:
  - Reuse the existing static top bar and CSS.
  - Render grouped command rows, separators, shortcuts or hints and selectable CLI text.
  - Keep all menu actions informational or navigational inside the page.
- Out:
  - Clipboard permissions, shell execution, fetch calls or any write path.
  - Adding a menu framework or shared command registry before more than this viewer needs it.

# Acceptance criteria
- AC1: Opening each menu shows grouped rows with visible shortcuts or hints and selectable CLI text.
- AC2: Menu rows do not call fetch, spawn a process, mutate report files or require a server.
- AC3: New visible menu labels are present in the i18n catalogue.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: Opening each menu shows grouped rows with visible shortcuts or hints and selectable CLI text.
- request-AC6 -> This backlog slice. Proof: AC2: Menu rows do not call fetch, spawn a process, mutate report files or require a server.

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

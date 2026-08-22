## item_037_fix_the_start_screen_s_layout_overflow_and_decide_its_command_affordance - Fix the start screen's layout overflow and decide its command affordance
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 85%
> Complexity: Medium
> Theme: Operator workflow and runtime integration
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-22 23:15:12

# AI Context
- Summary: (unfilled: replace before this doc is used)
- Keywords: fix, start, screen, layout, overflow, decide, command, affordance
- Use when: (unfilled: replace before this doc is used)
- Skip when: (unfilled: replace before this doc is used)

# Problem
- The start screen's three-column layout overflows its own modal at at least one common width.
- Its template cards show commands as plain text with no way to run them, even when the page is served.

# Scope
- In:
  - Fixing the overflow, verified with a rendered screenshot at common desktop widths.
  - A recorded decision (ADR amendment, new ADR, or explicit non-goal) on whether these specific commands become served-runnable, and matching UI either way.
- Out:
  - Any other viewer layout beyond this modal.

# Acceptance criteria
- AC1: No column's content pushes past the modal's right edge at common desktop widths.
- AC2: A decision is recorded and the start screen's template cards match it.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: No column's content pushes past the modal's right edge at common desktop widths.
- request-AC3 -> This backlog slice. Proof: AC2: A decision is recorded and the start screen's template cards match it.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_009_a_viewer_that_acts_on_what_it_shows_not_just_displays_it`
- Architecture decision(s): (none yet)
- Request: `req_008_make_the_viewer_s_start_screen_runbooks_and_file_references_actionable`
- Primary task(s): `task_022_deliver_the_viewer_actionability_pass`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

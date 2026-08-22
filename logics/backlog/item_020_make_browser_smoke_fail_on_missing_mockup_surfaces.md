## item_020_make_browser_smoke_fail_on_missing_mockup_surfaces - Make browser smoke fail on missing mockup surfaces
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
- Summary: Extend the browser smoke so missing menu, Runbooks, splash or Compare surfaces fail automatically.
- Keywords: browser, smoke, fail, missing, mockup, surfaces
- Use when: Updating viewer smoke checks, required selectors, interaction assertions or temporary screenshots.
- Skip when: Work requires pixel-perfect golden comparisons or a new browser-test framework.

# Problem
- The current smoke coverage can pass while major mockup surfaces are absent.
- Screenshots help manual review, but the automated check must assert the required states directly.

# Scope
- In:
  - Exercise menu opening, Runbooks workspace, Start splash and Compare wipe in the existing Chrome smoke path.
  - Assert stable selectors or visible state for each required surface.
  - Write screenshots only to a temporary path outside the repository.
- Out:
  - A broad pixel-diff framework.
  - New browser test dependencies when the existing smoke path is enough.

# Acceptance criteria
- AC1: One smoke command fails if menus, Runbooks, splash or Compare are missing.
- AC2: The smoke changes the comparison wipe value and verifies the visible state changed.
- AC3: No smoke screenshot or generated browser artifact is tracked by Git.

# AC Traceability
- request-AC5 -> This backlog slice. Proof: AC1: One smoke command fails if menus, Runbooks, splash or Compare are missing.
- request-AC6 -> This backlog slice. Proof: AC2: The smoke changes the comparison wipe value and verifies the visible state changed.

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

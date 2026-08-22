## item_040_root_cause_the_vehicle_demonstration_s_disappearing_glass_panes - Root-cause the vehicle demonstration's disappearing glass panes
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
- Keywords: root, cause, vehicle, demonstration, disappearing, glass, panes
- Use when: (unfilled: replace before this doc is used)
- Skip when: (unfilled: replace before this doc is used)

# Problem
- The vehicle asset's glass panes (windshield, side and rear windows) appear to be progressively lost across the demo chain's own operations.

# Scope
- In:
  - Tracing which operation(s) remove or merge the glass panes, using the real chain's own reports.
  - Either a fix that keeps them intact through the full chain, or an honest, documented explanation in the build script and README if keeping them intact would weaken a real lesson the chain teaches.
- Out:
  - Any change to the asset's other geometry.

# Acceptance criteria
- AC1: The specific operation(s) responsible are identified and named, with the real report data that shows it.
- AC2: Either the panes survive the full chain in a fresh run, or the build script and README explain why not.

# AC Traceability
- request-AC7 -> This backlog slice. Proof: AC1: The specific operation(s) responsible are identified and named, with the real report data that shows it.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_009_a_viewer_that_acts_on_what_it_shows_not_just_displays_it`
- Architecture decision(s): (none yet)
- Request: `req_008_make_the_viewer_s_start_screen_runbooks_and_file_references_actionable`
- Primary task(s): `task_022_deliver_the_viewer_actionability_pass`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.

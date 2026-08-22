## item_045_serve_the_viewer_payload_instead_of_baking_it_into_the_page - Serve the viewer payload instead of baking it into the page
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:37:30

# AI Context
- Summary: The payload comes from a route on the served page and from the generated file only when the page was opened from disk.
- Keywords: payload route, build-time snapshot, opened-from-disk fallback
- Use when: Changing where the page's data comes from.
- Skip when: Changing what the payload contains.

# Problem
- The payload is written into `work/viewer/data.js` when the command runs, so the page is a snapshot: reloading it cannot show a report that landed afterwards.

# Scope
- In:
  - A route that returns the payload the build already computes.
  - The client reading that route when it is served, and the generated file when it is not.
  - Keeping the generated fallback file exactly as it is for a page opened from disk.
- Out:
  - Response caching, ETags and conditional requests -- not yet worth their code at this payload size.
  - Any change to the payload's contents.

# Acceptance criteria
- AC1: A served page renders from the route, not from the generated file.
- AC2: A page opened from disk renders exactly as it does today.
- AC3: A report rendered before and after this change is identical.

# AC Traceability
- request-AC1 -> This backlog slice. Proof: AC1: A served page renders from the route, not from the generated file.
- request-AC12 -> This backlog slice. Proof: AC2: A page opened from disk renders exactly as it does today.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_011_a_viewer_that_stays_current_and_a_codebase_that_stays_divisible`
- Architecture decision(s): (none yet)
- Request: `req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds`
- Primary task(s): `task_024_deliver_the_live_viewer_and_the_module_structure`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

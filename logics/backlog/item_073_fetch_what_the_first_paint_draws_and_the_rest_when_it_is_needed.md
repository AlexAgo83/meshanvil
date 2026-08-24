## item_073_fetch_what_the_first_paint_draws_and_the_rest_when_it_is_needed - Fetch what the first paint draws, and the rest when it is needed
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 10%
> Complexity: Medium
> Theme: Viewer payload and first paint
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-25 00:23:17

# AI Context
- Summary: Measured at 623 KB before any click: 217 KB of reports for every sibling project with the active one duplicated, and 124 KB of runbook bodies nobody has opened. Renders are already lazy; the JSON is not. The cost is structural rather than large today, and it grows with every project and runbook added.
- Keywords: first paint payload, data.js size, lazy fetch, runbook bodies, sibling projects, placeholder, file protocol snapshot
- Use when: Changing what viewer_payload builds, or adding a fetch the page makes after its first paint.
- Skip when: The file:// snapshot is not a place to save bytes -- it has no server to fetch from and must stay whole.

# Problem
- The measured payload is 623 KB before anything is clicked: 217 KB of reports for every sibling project, with the active one duplicated, and 124 KB of runbook bodies nobody has opened.
- The cost is structural rather than large today, and it grows with every project and every runbook added.
- Renders are already lazy; the JSON is not.

# Scope
- In:
  - A first payload carrying the active project's reports, the project list without their reports, and runbook metadata without their bodies.
  - Fetching a project's reports when it is selected, and a runbook's body when it is opened. Neither is reachable today: `/api/data` returns everything and there is no route that returns one project or one document, so the routes are part of this item rather than assumed.
- Accepting that the served payload and the file:// payload become two shapes, and keeping both built from one place so they cannot drift apart unnoticed.
  - A placeholder in the region being filled, so a fetch reads as pending rather than empty.
  - Keeping the file:// snapshot whole: a page with no server still has everything it needs.
  - Checks: the payload's shape in the Python checks, and the placeholder and the fetch in the browser smoke.
- Out:
  - Pagination or virtualisation of long lists.
  - Caching across sessions, or a service worker.
  - Changing what a report contains.

# Acceptance criteria
- AC1: The first payload contains no report belonging to a project other than the active one, and no runbook body.
- AC2: Selecting another project fetches its reports and draws them, with a placeholder shown while the fetch is in flight.
- AC3: Opening a runbook fetches its body the first time and not again afterwards.
- AC4: The file:// snapshot still carries everything, and every screen works with no server.
- AC5: A Python check fails if a runbook body or a non-active project's reports reappear in the first payload.
- AC6: The routes that serve one project's reports and one document's body are guarded like every other route on that server, and refuse a foreign Host and a foreign Origin.
- AC7: Both payload shapes are produced by the same builder, and a check fails if one gains a field the other does not account for.

# AC Traceability
- request-AC6 -> This backlog slice. Proof: AC1: The first payload contains no report belonging to a project other than the active one, and no runbook body.
- request-AC9 -> This backlog slice. Proof: AC2: Selecting another project fetches its reports and draws them, with a placeholder shown while the fetch is in flight.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_015_a_viewer_that_keeps_up_with_the_work`
- Architecture decision(s): (none yet)
- Request: `req_016_make_the_viewer_s_outliner_refresh_and_annotations_hold_up_in_daily_use`
- Primary task(s): `task_029_deliver_the_viewer_s_fold_refresh_payload_and_annotation_work`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.

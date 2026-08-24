## item_072_keep_the_operator_s_choices_across_a_live_refresh - Keep the operator's choices across a live refresh
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 75%
> Complexity: Medium
> Theme: Viewer usability and live state
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-25 00:23:17

# AI Context
- Summary: Two independent problems behind one symptom. The bug: fetchData() assigns a whole new DATA, so the active project in the response replaces the one the operator selected. The design point: the events route sleeps for twenty times its own scan cost, so the viewer gets slower the more projects there are to watch.
- Keywords: fetchData, DATA.active, project selection lost, events cadence, adaptive backoff, selective repaint
- Use when: Touching how the page ingests a payload, or how often the server tells it something changed.
- Skip when: The work is about the size of the payload rather than what the page does with it -- that is the first-paint item, not this one.

# Problem
- fetchData() assigns a new DATA wholesale, so the active project carried in the response replaces the one the operator selected.
- The events route sleeps for twenty times the cost of its own scan, so the interval grows with the project count and the viewer gets slower the more there is to watch.
- A refresh repaints everything whatever changed, so a background event is visible as a flicker over work in progress.

# Scope
- In:
  - Preserving the selected project, the selected report and the fold state across a refresh, by merging the new payload into the page's state rather than replacing it.
  - A declared, bounded interval for the events channel that does not derive from its own scan cost.
  - Repainting only what the change touched, where the change can be identified.
  - Checks: the merge rule in viewer/src without a DOM, the preserved selection in the browser smoke, and the events cadence in the Python checks.
- Out:
  - Replacing the events transport, or adding a websocket.
  - Incremental payloads over the wire -- this item is about what the page does with a payload, not its size.
  - Undo, or any history of operator choices.

# Acceptance criteria
- AC1: Selecting a project, then triggering a change on disk, leaves the selected project active.
- AC2: The selected report and the fold state survive the same sequence. The fold state is keyed by chain, which item_071 changes: this AC is verified against that keying, not the group keying it replaces.
- AC3: The events channel's interval is a declared value, and adding sibling projects does not change it.
- AC4: A refresh that changes nothing leaves the DOM of the outliner and the canvas untouched.
- AC5: A Python check fails if the events cadence is derived from the scan's own duration.

# AC Traceability
- request-AC4 -> This backlog slice. Proof: AC1: Selecting a project, then triggering a change on disk, leaves the selected project active.
- request-AC5 -> This backlog slice. Proof: AC2: The selected report and the fold state survive the same sequence.
- request-AC9 -> This backlog slice. Proof: AC3: The events channel's interval is a declared value, and adding sibling projects does not change it.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_015_a_viewer_that_keeps_up_with_the_work`
- Architecture decision(s): (none yet)
- Request: `req_016_make_the_viewer_s_outliner_refresh_and_annotations_hold_up_in_daily_use`
- Primary task(s): `task_029_deliver_the_viewer_s_fold_refresh_payload_and_annotation_work`

# Priority
- Priority: High
- Rationale: Set by scaffold input or defaulted for grooming.

## item_046_push_change_to_the_open_page_over_a_standard_library_event_stream - Push change to the open page over a standard-library event stream
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 00:53:33

# AI Context
- Summary: A standard-library event stream tells the open page which component changed, detected by a bounded signature poll, with a self-throttling fallback where the stream is unavailable.
- Keywords: server-sent events, signature poll, component notice, adaptive interval, fallback timer
- Use when: Working on how the page learns that something changed.
- Skip when: Working on what the page does with the data once it has it.

# Problem
- `adr_004` promised auto-refresh and nothing implements it, so watching a chain run means restarting the server and reopening the page for every report.

# Scope
- In:
  - One event-stream route whose change detection is a standard-library signature poll over the report directory, the cached setup result and the runbooks.
  - Emitting which component changed rather than the changed data, with the client refetching only that.
  - A bounded, measured detection cost with an adaptive interval, and a self-throttling fallback where the event stream is unavailable.
  - Clean shutdown: no timer and no connection outliving the page.
  - Retiring or repurposing the View menu's `Refresh viewer` row, which `adr_007` left copy-only pending a slice that gives it a real target: once the page refreshes itself, a row telling the operator to re-run the command is stale advice.
- Out:
  - A file-watching dependency, and a websocket where one direction suffices.
  - Pushing anything other than change notices -- no data travels on the stream.

# Acceptance criteria
- AC1: A report written while the page is open appears without a restart or a reload, within a few seconds.
- AC2: A removed or modified report is reflected the same way.
- AC3: Detection uses the standard library only and its idle cost is measured and stated against a bound.
- AC4: The stream carries component names, not data, and no client path reloads the page on a data change.
- AC5: With the event stream unavailable, the fallback still converges and throttles itself against its own last refresh cost.
- AC6: Closing the page leaves no live timer and no live connection.
- AC7: The `Refresh viewer` row is gone or does something real; no row tells the operator to re-run a command the page now does for itself.

# AC Traceability
- request-AC2 -> This backlog slice. Proof: AC1: A report written while the page is open appears without a restart or a reload, within a few seconds.
- request-AC3 -> This backlog slice. Proof: AC2: A removed or modified report is reflected the same way.
- request-AC4 -> This backlog slice. Proof: AC3: Detection uses the standard library only and its idle cost is measured and stated against a bound.
- request-AC5 -> This backlog slice. Proof: AC4: The stream carries component names, not data, and no client path reloads the page on a data change.

- request-AC17 -> This backlog slice. Proof: AC7: The `Refresh viewer` row is gone or does something real; no row tells the operator to re-run a command the page now does for itself.

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

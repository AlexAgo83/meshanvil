## item_058_stop_the_served_viewer_listing_work_and_holding_threads_for_absent_peers - Stop the served viewer listing work/ and holding threads for absent peers
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Low
> Theme: Host boundary
> Reminder: Update status/understanding/confidence/progress and linked request/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 10:31:28

# AI Context
- Summary: Two small refusals on the served viewer: no directory listing under work/, and a write on every /api/events poll so a departed peer is detected instead of holding its thread.
- Keywords: served, viewer, listing, work, holding, threads, absent, peers
- Use when: working on what the served viewer exposes by default or on the lifetime of an events connection.
- Skip when: replacing mtime polling with a platform watcher, or adding a connection cap before the write-per-poll check shows one is needed.

# Problem
- The handler serves root/work through SimpleHTTPRequestHandler with directory listings left on, so a GET of the served root enumerates in/, out/, ops/ and renders/ -- and SECURITY.md names source file paths as the sensitive part of this work.
- /api/events writes only when a signature changes, so a connection whose peer has gone is never written to and its thread is never released; the server caps neither threads nor connections.
- The page never needs a directory listing: it fetches /api/data.
- Only a directory with no index.html reaches the listing branch, so refusing it leaves work/viewer/ serving its page as before; work/ itself, work/in/, work/out/ and work/renders/ are the directories that currently enumerate.
- A write to a departed peer can succeed once before the connection is seen as gone, so detection may take two polls rather than one; the check has to allow for that rather than assert on the first.

# Scope
- In:
  - Refusing a directory request under the served root instead of rendering a listing.
  - Writing on every poll of /api/events so a broken peer surfaces on the next turn and the existing handler releases the thread.
  - Selfchecks for both, with pytest wrappers.
- Out:
  - Replacing mtime polling with a platform watcher, which the code already marks as a later step gated on profiling.
  - A connection cap, a thread pool or a stream lifetime, unless the write-per-poll check shows one is still needed.
  - Serving anything other than work/, or changing which files the page fetches.

# Acceptance criteria
- AC1: A GET for the served root and for a directory beneath it returns 404, while the viewer page and its assets still load.
- AC2: An /api/events connection whose peer has closed is released without any report or runbook changing.

# AC Traceability
> Shared proof: AC5, AC8
- request-AC4 -> This backlog slice. Proof: AC1: A GET for the served root and for a directory beneath it returns 404, while the viewer page and its assets still load.
- request-AC5 -> This backlog slice. Proof: AC2: An /api/events connection whose peer has closed is released without any report or runbook changing.
- request-AC8 -> This backlog slice. Proof: AC2: An /api/events connection whose peer has closed is released without any report or runbook changing.

# Decision framing
- Product framing: Not needed
- Architecture framing: Not needed

# Links
- Product brief(s): `prod_013_a_host_boundary_that_matches_its_own_documentation`
- Architecture decision(s): (none yet)
- Request: `req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented`
- Primary task(s): `task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution`

# Priority
- Priority: Medium
- Rationale: Set by scaffold input or defaulted for grooming.

# Tasks
- `task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution`

# Notes
- Task `task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution` was finished via `logics-manager flow finish task` on 2026-08-23.

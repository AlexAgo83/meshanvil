## req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented - Make the served viewer, prune and project resolution behave the way they are documented
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 95%
> Confidence: 90%
> Complexity: Medium
> Theme: Host boundary
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 10:31:27

# AI Context
- Summary: Closes the seven findings captured in req_012: the served viewer answers requests that did not come from its page, prune can delete outside the project, and two labels contradict the behaviour they name. Host-side only, no Blender.
- Keywords: served, viewer, prune, project, resolution, behave, way, they, documented
- Use when: planning or implementing any change to the served viewer's request boundary, to what prune is allowed to delete, or to how the active project is chosen and named.
- Skip when: working on engine-side geometry under tools/ or pipeline/, on the viewer's interface or payload shape, or on the hand-armed bl_cmd bridge described in run_001.

# Needs
- The served viewer must refuse a request that did not come from its own page, so that the boundary SECURITY.md and adr_007 describe is the one the code enforces.
- SECURITY.md and adr_007 must describe the boundary that exists: how the port is chosen, what the run token proves, and what a cross-origin request gets.
- prune must never delete a file outside the project it was asked to prune, and neither prune nor prune --dry-run may end in an unhandled traceback.
- The served viewer must not enumerate work/ to a caller, and must not hold a thread for a connection whose peer has gone.
- An interrupted run must leave no engine process behind, and the rule that chose the active project must be labelled and documented as what it actually is.

# Context
- Findings captured in req_012 from a read-only review at commit 3e13ed0; make check and make logics were green at that commit.
- The run token cannot be a secret against a local process: work/viewer/data.js is a file on disk and the whole of work/ is the served directory. What it can prove is that a request came from the page this server generated, which is a browser-facing property.
- viewer/src/app.js replaces its boot payload with GET /api/data and derives its served flag from run_token, so removing the token from that route without a replacement signal breaks the live refresh.
- stable_port derives the port from a SHA-256 of the project path, so the port is predictable once the project location is known; nothing else on the server inspects Host, Origin or Referer.
- The custom X-Meshanvil-Token header already forces a CORS preflight on POST, which is the property currently preventing blind cross-origin writes. It should be a stated defence rather than an incidental one.
- Every behaviour this request changes is host-side and needs no Blender, so each one belongs in scripts/selfcheck.py with a thin pytest wrapper in tests/ -- the suite that already gates CI.
- make_server takes port=0 by default and both scripts/selfcheck.py and tests/test_viewer.py call it that way, so the handler cannot know its own origin when the class is defined. The guard has to read the port from the bound socket at request time.
- work/viewer/server.json, the registry written so a second launch reuses a running viewer, carries the same token and sits inside the served directory. It is a third read path alongside /api/data and work/viewer/data.js, and the reason the guard has to cover static files rather than only the routes.
- Reusing a running viewer builds a fresh data.js whose token the running server does not accept; the page recovers only because /api/data returns the running server's own token. That is a second reason removing the token from that route is out of scope.
- doctor.check reports the resolution rule as project.resolved_by in work/doctor.json, which the viewer displays and an agent reads. Renaming the fallback rule changes a machine-readable value, not only a label, and item_010's rule that identifiers are never translated applies to it.
- adr_007's decision -- closed command set, per-launch token, single flight -- is not being reversed. What is wrong is its description of what the token guarantees. Amend that description and the consequences; supersede only if the decision itself turns out to need changing, which is the convention adr_007 itself followed with adr_003.

# Acceptance criteria
- AC1: A request whose Host is not a loopback name, or whose Origin is present and is not this server's own origin, is refused on every route including /api/ping, /api/data, /api/events, /run and static files.
- AC2: SECURITY.md and adr_007 state how the port is chosen, what the run token proves and does not prove, and what a cross-origin or rebound request receives; no claim in either document contradicts the code.
- AC3: prune ignores any report output path that is not inside the active project, and both prune and prune --dry-run complete without an unhandled exception on such a report.
- AC4: A GET for a directory under the served root returns 404 rather than a listing, and the viewer page still loads and refreshes.
- AC5: An /api/events connection whose peer has gone is released without waiting for a report or runbook to change.
- AC6: Interrupting a run terminates the engine process before the runner re-raises, and what the interrupt leaves on disk is stated in the runner's own docstring.
- AC7: The rule name and module documentation for the fallback project resolution describe the directory that is actually returned.
- AC8: Each accepted change leaves one runnable check in scripts/selfcheck.py, reached by a pytest wrapper in tests/, and make check stays green.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_013_a_host_boundary_that_matches_its_own_documentation`
- Architecture decision(s): (none yet)

# References
- logics/request/req_012_review_findings_served_viewer_boundary_prune_safety_and_project_resolution.md
- meshanvil/viewer_server.py
- meshanvil/viewer_payload.py
- meshanvil/viewer_routes/events.py
- meshanvil/prune.py
- meshanvil/runner.py
- meshanvil/paths.py
- scripts/selfcheck.py
- SECURITY.md
- logics/architecture/adr_007_let_the_served_viewer_execute_a_closed_command_set.md

# Backlog
- `item_056_refuse_a_served_viewer_request_that_did_not_come_from_its_own_page`
- `item_057_keep_prune_inside_the_project_it_was_asked_to_prune`
- `item_058_stop_the_served_viewer_listing_work_and_holding_threads_for_absent_peers`
- `item_059_leave_nothing_running_and_nothing_mislabelled_after_an_interrupted_run`

## req_010_make_the_viewer_refresh_itself_and_give_the_code_a_module_structure_that_holds - Make the viewer refresh itself and give the code a module structure that holds
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Complexity: High
> Theme: Runtime architecture and code structure
> Reminder: Update status/understanding/confidence and linked backlog/task references when you edit this doc.
> Indicators reviewed: 2026-08-23 01:27:27

# AI Context
- Summary: The served page becomes a live view onto the reports directory instead of a build-time snapshot, and both sides of the viewer gain a module structure, a checked size budget and a real test layout.
- Keywords: server-sent events, mtime signature poll, payload route, module split by screen, line budget, pytest layout, adr_004 amendment
- Use when: Deciding how the viewer stays current, or how the viewer's code is divided and checked.
- Skip when: Deciding what the viewer displays or what a report contains -- req_000 and adr_001 hold that.

# Needs
- `meshanvil view` builds and opens a page from disk by default and only serves behind `--serve`, so the mode that can refresh itself is the one nobody gets unless they ask. Every launch also starts a fresh server on port 0, so the address changes every time -- an open tab, a bookmark and a second `meshanvil view` all point somewhere that no longer exists, and nothing notices that a viewer for this project is already running.
- `adr_004` states that `meshanvil view --serve` starts a server `for auto-refresh`. Nothing auto-refreshes: there is no watcher, no event stream and no polling anywhere in `meshanvil/viewer.py` or `viewer/viewer.js`. The promise is documented and was never built, so an operator watching a chain run has to stop the server, re-run the command and reopen the page to see the report that just landed.
- Even a manual browser refresh shows nothing new: the payload is baked into `work/viewer/data.js` at build time, so the page is a snapshot of the moment the command ran rather than a view onto the reports directory.
- `viewer/viewer.js` is 908 lines in one file covering every screen, every renderer and every event handler. Each slice that touches the viewer -- and the last four have -- edits the same file, and nothing states when it has grown too large.
- `meshanvil/viewer.py` is 199 lines doing three unrelated jobs: computing the payload, serving it over HTTP, and launching a browser. It is the file the next three endpoints (a data route, an event stream, and the open/reveal route `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls` needs) would all land in.
- There is no test directory and no test runner. `scripts/selfcheck.py` is 353 lines of hand-rolled asserts covering the whole host codebase in one file, so a single module's behaviour has nowhere of its own to be checked and a failure names the script rather than the unit.

# Context
- `logics-manager` treats this as a registry problem rather than a port problem: its viewer registry module keeps one live viewer per repository root, guarded by a cross-process file lock, with a liveness probe endpoint so a registration left behind by a killed process is reclaimed instead of believed. That is the shape to follow -- reuse-if-alive, reclaim-if-not -- and it is what makes a stable address safe to promise.
- `logics-manager` (../logics-manager) solves the same refresh problem with stdlib only and is the reference to follow rather than reinvent: one `GET /api/events` server-sent-event endpoint whose change detection is a cheap mtime/signature poll (no watchdog dependency, no websocket), emitting *component names* rather than data, with the client refetching only what changed and never calling `location.reload()`, and a self-throttling timer as the fallback where the browser has no event-stream support. Its poll sleep is duty-cycle adaptive so detection never costs more than a fraction of a core.
- What is deliberately NOT worth copying from `logics-manager` at this scale: ETag/304 handling, a status cache with a TTL, and its roughly ninety endpoints. Its payload is large and remote-backed; meshanvil's is a directory of small JSON files. Those are additions to make when a rebuild measurably costs something, not now.
- `logics-manager` also shows the structural conventions worth adopting: client modules split by screen rather than by layer (no per-layer components, api or store directories), server route modules exposing `handle_get(handler, route, parsed) -> bool` so a new endpoint never grows an existing file, and a per-file line budget enforced by a script with a registry of justified exceptions rather than by convention.
- The build-step question is the hard constraint, not a preference: Chrome refuses `import` from a page opened from disk, so native ES modules would break `meshanvil view`'s default mode. Bundling is therefore required to split the client at all, and bundling contradicts `adr_004`'s no-build-step stance -- which makes it an ADR-level decision. The alternative considered and rejected was hand-writing a small concatenator inside `build()` to avoid the dependency; that is more code to own than the dependency it avoids.
- Client unit tests are deliberately out of scope for this pass. While the client modules are DOM assembly, `scripts/viewer_smoke.py` already covers them end to end; a unit runner is worth adding when a module carries real logic of its own (the Markdown renderer is the first candidate).
- This request should land before `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls` is implemented. `req_009_turn_the_viewer_s_file_references_and_command_rows_into_direct_translated_controls` rewrites large parts of `viewer/viewer.js`; doing it first means rewriting the same code twice.

# Acceptance criteria
- AC1: The served page's payload is fetched from the server rather than read from a build-time file, and a page opened from disk keeps working exactly as it does today from its generated fallback.
- AC2: A served page reflects a new, changed or removed report without the operator restarting the server or reloading the page, within a few seconds of the file landing.
- AC3: Change detection uses the standard library only -- no file-watching dependency -- and its cost is bounded so that an idle viewer does not consume a meaningful share of a core; the bound is stated and measured, not asserted.
- AC4: The event stream carries what changed, not the changed data, and the client refetches only the affected part; no code path in the client reloads the whole page on a data change.
- AC5: A client with no event-stream support still converges on fresh data through a self-throttling fallback, and neither path leaves a timer or a connection running after the page is closed.
- AC6: `adr_004` is amended (or superseded) to record that the auto-refresh it promised now exists and how, that the served page is now the default mode with the opened-from-disk one behind a flag, and the build step the client split requires -- with the rejected alternative named.
- AC7: The client is split into modules by screen, each within a stated per-file line budget, with the budget enforced by a check in `make check` and any exception carried in a registry with its justification.
- AC8: The client bundle is produced by a build step, committed, and a check fails when the committed bundle no longer matches its sources.
- AC9: `meshanvil/viewer.py`'s three jobs -- payload, HTTP serving, host interaction -- live in separate modules, and adding a route does not require editing the module that dispatches them.
- AC10: The host code has a test directory with a runner, at least one test module per host module, and `make check` runs it; `scripts/selfcheck.py`'s coverage is carried over rather than dropped, and a failure names the unit that failed.
- AC11: `scripts/viewer_smoke.py` still passes end to end against the restructured client and server, and covers the live-refresh path itself.
- AC13: `meshanvil view` with no flag starts a served page; the build-and-open-from-disk mode stays reachable behind an explicit flag and behaves exactly as it does today.
- AC14: With a viewer already running for this project, the command opens that one instead of starting a second process, and says which of the two it did.
- AC15: A project's viewer address is stable across launches, so a tab left open or a bookmark keeps working; an address already taken by something else is reported rather than silently reassigned.
- AC16: A registration left behind by a viewer that died is reclaimed rather than believed, and two projects can each have a viewer at once without colliding.
- AC17: The View menu's `Refresh viewer` row -- left copy-only by `adr_007` pending a slice that gives it a real target -- is gone or does something real; no row tells the operator to re-run a command the page now performs for itself.
- AC12: Nothing in this request changes what the viewer shows or what an operation reports; a report rendered before and after is identical.

# Definition of Ready (DoR)
- [x] Problem statement is explicit and user impact is clear.
- [x] Scope boundaries (in/out) are explicit.
- [x] Acceptance criteria are testable.
- [x] Dependencies and known risks are listed.

# Companion docs
- Product brief(s): `prod_011_a_viewer_that_stays_current_and_a_codebase_that_stays_divisible`
- Architecture decision(s): (none yet)

# References
- meshanvil/viewer.py
- viewer/viewer.js
- viewer/index.html
- scripts/selfcheck.py
- scripts/viewer_smoke.py
- Makefile
- package.json
- tsconfig.json
- adr_003
- adr_004
- adr_007
- req_009

# Backlog
- `item_045_serve_the_viewer_payload_instead_of_baking_it_into_the_page`
- `item_046_push_change_to_the_open_page_over_a_standard_library_event_stream`
- `item_047_split_the_viewer_host_module_into_payload_server_and_host_interaction`
- `item_048_split_the_client_by_screen_behind_a_committed_checked_bundle`
- `item_049_give_the_host_code_a_test_layout_with_one_module_per_host_module`, `item_050_reuse_a_running_viewer_and_keep_its_address_stable`

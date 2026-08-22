## task_020_let_the_viewer_run_the_commands_it_already_shows_when_it_is_served - Let the viewer run the commands it already shows, when it is served
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: Claude
> Indicators reviewed: 2026-08-22 17:28:27

# AI Context
- Summary: Orchestrates the served-viewer execution reversal: the superseding ADR first, then the server endpoint, then the client wiring, each validated before the next, with file:// behaviour and the two out-of-scope commands confirmed unchanged at closeout.
- Keywords: orchestration, served viewer, adr supersession, closed command execution
- Use when: planning or sequencing this slice, or checking what remains before closeout.
- Skip when: the work is about a command outside the closed set, or about the plain file:// viewer.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 1. Write the superseding ADR first: the exact boundary (localhost-only, per-launch token, one command at a time, closed command set) decided before any code depends on it.
- [x] 2. Add the run endpoint to the existing --serve server: token check, closed command dispatch, single-flight guard, subprocess of bin/meshanvil.
- [x] 3. Thread the per-launch token into data.js next to the other build-time payload fields.
- [x] 4. Wire the three in-scope menu rows to the endpoint on a served page, rendering stdout/stderr/exit code; confirm file:// pages and the two out-of-scope rows are unchanged.
- [x] 5. Extend viewer_smoke (served mode) and add a host-side check for the endpoint's token and single-flight refusal.
- [x] 6. Mark adr_003 Superseded, cross-link it to the new ADR, and update adr_004's consequence note about the reversal cost.
- [x] 7. Run make check, the fixture check and both smokes (file:// and --serve) before closeout.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server`
- `item_033_show_a_command_s_own_output_where_its_text_used_to_sit`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented in b6d4ec2 (adr_007 written, adr_003 superseded in part), e4b3c21 (POST /run: per-launch token, closed RUNNABLE set, single-flight lock, subprocess of bin/meshanvil) and 47ec28c (SERVED detection, the three in-scope rows call runCommand() and render stdout/stderr/exit_code; file:// and the two out-of-scope rows unchanged). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py (file:// pass and the new check_served() pass against a real --serve subprocess) -- all passed. Source: `47ec28c`
- request-AC2 -> This task. Proof: Implemented in e4b3c21: a random token generated per server launch (secrets.token_urlsafe), threaded through build()'s run_token payload field, required as X-Meshanvil-Token on every /run request; missing or mismatched is refused with 401 before any subprocess starts. Validated with curl (wrong token, missing token) and check_run_endpoint in scripts/selfcheck.py. Source: `e4b3c21`
- request-AC3 -> This task. Proof: Implemented in e4b3c21: RUNNABLE is a closed dict (list/doctor/prune --dry-run); a command not in it is refused 400 before subprocess.run, and the request body contributes nothing else to the argument list. Validated with curl (`{"command":"rm -rf /"}` -> 400) and check_run_endpoint. Source: `e4b3c21`
- request-AC4 -> This task. Proof: Implemented in e4b3c21: ThreadingHTTPServer (replacing the prior single-threaded TCPServer) plus a non-blocking threading.Lock in the handler -- a concurrent request is refused 409, not queued, while the in-flight one still returns 200. Verified by hand with two concurrent curl calls (200 then 409) and by check_run_endpoint's race (a slow subprocess.run stub held via threading.Event). Source: `e4b3c21`
- request-AC5 -> This task. Proof: Implemented in 47ec28c: `Refresh viewer` and `Create a runbook <report-id>` were left with data-copy only, no data-run attribute; item_033's scope_out records the cut explicitly rather than dropping it silently. Source: `47ec28c`
- request-AC6 -> This task. Proof: Implemented in b6d4ec2: adr_003's Status set to Superseded via `logics-manager sync update-indicators --status Superseded`, cross-linked both directions with adr_007_let_the_served_viewer_execute_a_closed_command_set, and adr_004 given a consequence note that --serve now carries this endpoint. Source: `b6d4ec2`

# Validation
- `make check` -- compile, types, selfcheck (incl. check_run_endpoint), i18n, hygiene: all green.
- `python3 scripts/fixture_check.py` -- 7 reports, defects found unaided.
- `python3 scripts/viewer_smoke.py` -- file:// pass and the served-mode pass (check_served: real `meshanvil view --serve` subprocess, real headless Chrome, real `list` execution asserted in the DOM): both green.
- Manual verification over a real socket (curl) and a real browser: valid token/command runs and returns stdout/stderr/exit_code; wrong token, missing token, and an out-of-set command are refused (401/401/400) before any subprocess starts; two concurrent requests return 200 and 409, never two 200s; the served page renders `list`'s real output inline (screenshot-verified).
- command: `make check && python3 scripts/fixture_check.py && python3 scripts/viewer_smoke.py` | result: passed | date: 2026-08-22
- Finish workflow executed on 2026-08-22.
- Linked backlog/request close verification passed.

# Report
- Three commits: `b6d4ec2` (adr_007, adr_003 superseded in part), `e4b3c21` (server-side run endpoint), `47ec28c` (client wiring + served-mode smoke). adr_003 stands unchanged for every command outside the closed set and for the whole file:// viewer.
- Finished on 2026-08-22.
- Linked backlog item(s): `item_032_run_a_closed_set_of_commands_from_the_served_viewer_s_own_server`, `item_033_show_a_command_s_own_output_where_its_text_used_to_sit`
- Related request(s): `req_006_let_the_viewer_run_the_commands_it_already_shows_when_it_is_served`

# Links
- Request: `req_006_let_the_viewer_run_the_commands_it_already_shows_when_it_is_served`
- Product brief(s): `prod_007_a_served_viewer_that_can_run_what_it_already_shows`
- Architecture decision(s): `adr_007_let_the_served_viewer_execute_a_closed_command_set` (supersedes `adr_003_the_viewer_reads_the_command_acts` in part)

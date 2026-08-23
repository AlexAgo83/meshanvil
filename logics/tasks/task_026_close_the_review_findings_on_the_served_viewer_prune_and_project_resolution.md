## task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution - Close the review findings on the served viewer, prune and project resolution
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 95%
> Confidence: 90%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: codex
> Indicators reviewed: 2026-08-23 10:31:27

# AI Context
- Summary: The ordered plan for req_013: settle adr_007 first, then the origin guard, prune containment, the two viewer refusals, the runner and paths labels, each with a selfcheck.
- Keywords: close, review, findings, served, viewer, prune, project, resolution
- Use when: implementing req_013, in the order the plan gives.
- Skip when: scoping new work, or implementing anything outside the four backlog items this task carries.

# Context
- Four host-side slices closing the seven findings req_012 captured at commit 3e13ed0. No Blender is needed for any of them; make check is the gate.
- The order matters once: adr_007's description of what the token guarantees has to be settled before the guard that replaces it is written. Everything after step 4 is independent and can land in any order.
- Three traps that are not visible from the findings alone: make_server binds port 0 in both callers under test, so the guard must read its port from the bound socket; work/viewer/server.json carries the token inside the served directory, so the guard has to cover static files; and doctor.check writes the resolution rule into work/doctor.json, so renaming it changes a value an agent parses.
- Reproduce the two destructive findings on a scratch project outside the repository. Never against this repository's work/.

# Plan
- [x] 1. Read req_012 for the observed evidence behind each finding, then reproduce the two destructive ones on a scratch project outside the repository: the unauthenticated token read and the out-of-project prune. Do not run either against this repository's work/.
- [x] 2. Settle adr_007 first: amend its boundary description and consequences to say that the run token proves a request came from the generated page rather than being a secret, and that the origin guard is the defence against a rebound name. Its decision -- closed command set, per-launch token, single flight -- is not reversed, so amend rather than supersede; write a superseding ADR only if the decision itself turns out to need changing.
- [x] 3. Add the origin guard to ViewerHandler ahead of route dispatch in both do_GET and do_POST, covering /api/ping and the static branch as well as the routes; refuse an absent or non-loopback Host and a foreign Origin. Read the port from self.server.server_address at request time -- make_server defaults to port 0 and both test callers use that default.
- [x] 4. Rewrite the --serve section of SECURITY.md against the code as it then stands: the port rule, the token's guarantee, the cross-origin answer, and the directory-listing behaviour once the next step lands.
- [x] 5. Add the containment condition to prune.candidates and confirm both prune and prune --dry-run survive a report pointing outside the project, with the file intact.
- [x] 6. Refuse directory requests under the served root, and write on every /api/events poll so a gone peer is detected on the next turn. Only a directory without index.html reaches the listing branch, so work/viewer/ is unaffected; allow up to two polls for the broken peer to surface.
- [x] 7. Hold the engine Popen so the existing BaseException path kills it before unlinking the report, and record in the docstring what an interrupt leaves.
- [x] 8. Rename the fallback resolution rule and correct the paths docstring, following the name through doctor.check's project.resolved_by field, the cli.project.where message, the locale catalogues and the existing assertion in scripts/selfcheck.py. The new name is an identifier an agent reads, so it is not translated.
- [x] 9. Add one check per change to scripts/selfcheck.py with its thin pytest wrapper in tests/, following the shape the existing checks use.
- [x] 10. Run make check and make logics, plus scripts/viewer_smoke.py in served mode; run scripts/fixture_check.py if a Blender is available and say so if it is not.
- [x] 11. Record in the task which findings were closed by which change, and which of req_012's context notes were confirmed or contradicted along the way.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_056_refuse_a_served_viewer_request_that_did_not_come_from_its_own_page`
- `item_057_keep_prune_inside_the_project_it_was_asked_to_prune`
- `item_058_stop_the_served_viewer_listing_work_and_holding_threads_for_absent_peers`
- `item_059_leave_nothing_running_and_nothing_mislabelled_after_an_interrupted_run`

# Definition of Done (DoD)
- [x] Each of req_012's seven findings is either closed by a named change or recorded as deliberately left, with the reason.
- [x] Every claim in the --serve section of SECURITY.md and in adr_007's boundary description can be pointed at a line of code or a selfcheck.
- [x] Each closed finding has a check in scripts/selfcheck.py, reached from tests/, that fails if the behaviour comes back.
- [x] make check and make logics are green, and scripts/viewer_smoke.py passes in served mode.
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: `check_viewer_origin_and_listing` refuses bad Host and bad Origin before `/api/ping`, `/api/data`, `/api/events`, `/run`, `/file`, and static files; validated by `python3 scripts/selfcheck.py`, `pytest tests/test_viewer.py`, `make check`, and commit `00a4997`.
- request-AC2 -> This task. Proof: SECURITY.md and adr_007 now state the bound-port Host rule, the same-origin Origin rule, and that the token proves page origin after the guard rather than local secrecy; validated by `logics-manager lint --require-status`, `logics-manager audit --group-by-doc`, and commit `00a4997`.
- request-AC3 -> This task. Proof: `prune.candidates` skips outputs outside the project root; `check_prune` covers dry-run and deleting prune on an outside path and confirms the file remains; validated by `python3 scripts/selfcheck.py`, `pytest tests/test_prune.py`, `make check`, and commit `00a4997`.
- request-AC4 -> This task. Proof: `ViewerHandler.list_directory` returns 404, while `check_viewer_origin_and_listing` confirms `/` and `/in/` are refused and `/viewer/index.html` still loads; validated by `python3 scripts/selfcheck.py`, `pytest tests/test_viewer.py`, `make viewer-smoke`, and commit `00a4997`.
- request-AC5 -> This task. Proof: `/api/events` writes a poll comment and flushes every unchanged poll; `check_events_releases_gone_peer` raises `BrokenPipeError` on the next write and returns without report/runbook changes; validated by `python3 scripts/selfcheck.py`, `pytest tests/test_viewer.py`, `make check`, and commit `00a4997`.
- request-AC6 -> This task. Proof: `runner.run` keeps the `Popen`, terminates or kills it on `BaseException`, removes the empty report, re-raises, and documents that the job remains while the target lock is released; validated by `check_runner_interrupt_stops_engine`, `pytest tests/test_runner.py`, `make check`, and commit `00a4997`.
- request-AC7 -> This task. Proof: `paths.resolve` returns the searched directory as `current_directory` when no marker is found, and the module docs describe current-directory fallback rather than installation fallback; validated by `check_projects`, `pytest tests/test_paths.py`, `make check`, and commit `00a4997`.
- request-AC8 -> This task. Proof: each accepted behavior has a `scripts/selfcheck.py` check reached by pytest wrappers in `tests/`; `make check`, `make viewer-smoke`, `python3 scripts/fixture_check.py`, lint, audit, and flow validate all passed before closeout; source commit `00a4997`.

# Validation
- `python3 scripts/selfcheck.py` passed.
- `python3 -m pytest -q tests/test_viewer.py tests/test_prune.py tests/test_runner.py tests/test_paths.py` passed: 16 tests.
- `make check` passed: compileall, types, viewer bundle, line budget, 24 pytest tests, i18n, hygiene.
- `make viewer-smoke` passed against the served viewer.
- `python3 scripts/fixture_check.py` passed: 7 reports, defects found unaided.
- `logics-manager lint --require-status` passed.
- `logics-manager audit --group-by-doc` passed with warnings only.
- `logics-manager flow validate task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution` passed.
- Implemented in 00a4997. Passed: python3 scripts/selfcheck.py; python3 -m pytest -q tests/test_viewer.py tests/test_prune.py tests/test_runner.py tests/test_paths.py; make check; make viewer-smoke; python3 scripts/fixture_check.py; logics-manager lint --require-status; logics-manager audit --group-by-doc; logics-manager flow validate task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution; validate-closeout.
- Finish workflow executed on 2026-08-23.
- Linked backlog/request close verification passed.

# Report
- Closed N1/N2 by putting Host/Origin validation before `/api/ping`, `/api/data`, `/api/events`, `/run`, `/file`, and static files; adr_007 and SECURITY.md now say the token is page-origin proof after the origin guard, not a local secret.
- Closed N3 by keeping prune candidates inside the resolved project root; dry-run and deleting prune both ignore outside paths and leave the outside file intact.
- Closed N4 by refusing served-root directory listings while leaving `work/viewer/index.html` loadable.
- Closed N5 by writing an SSE comment on every `/api/events` poll so a gone peer is released without report or runbook changes.
- Closed N6 by retaining the engine `Popen` and terminating or killing it on `BaseException` before the empty claimed report is removed; the runner docstring states the job file remains and the target lock is released.
- Closed N7 by renaming the fallback project resolution rule to `current_directory` and updating the paths documentation and selfcheck assertion.
- Confirmed the req_012 context note that the served token is exposed in served viewer data; contradicted the stale SECURITY.md claim that randomness of the port or token secrecy was the boundary.
- Finished on 2026-08-23.
- Linked backlog item(s): `item_056_refuse_a_served_viewer_request_that_did_not_come_from_its_own_page`, `item_057_keep_prune_inside_the_project_it_was_asked_to_prune`, `item_058_stop_the_served_viewer_listing_work_and_holding_threads_for_absent_peers`, `item_059_leave_nothing_running_and_nothing_mislabelled_after_an_interrupted_run`
- Related request(s): `req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented`

# Links
- Request: `req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented`
- Product brief(s): `prod_013_a_host_boundary_that_matches_its_own_documentation`
- Architecture decision(s): (none yet)

## task_026_close_the_review_findings_on_the_served_viewer_prune_and_project_resolution - Close the review findings on the served viewer, prune and project resolution
> From version: 0.1.0
> Schema version: 1.0
> Status: Ready
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.

# AI Context
- Summary: The ordered plan for req_013: settle adr_007 first, then the origin guard, prune containment, the two viewer refusals, the runner and paths labels, each with a selfcheck.
- Keywords: close, review, findings, served, viewer, prune, project, resolution
- Use when: implementing req_013, in the order the plan gives.
- Skip when: scoping new work, or implementing anything outside the four backlog items this task carries.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Read req_012 for the observed evidence behind each finding, then reproduce the two destructive ones on a scratch project outside the repository: the unauthenticated token read and the out-of-project prune. Do not run either against this repository's work/.
- [ ] 2. Amend adr_007 first: decide and write down that the run token proves a request came from the generated page rather than being a secret, and that the origin guard is the defence against a rebound name. The code that follows depends on that being settled.
- [ ] 3. Add the origin guard to ViewerHandler ahead of route dispatch in both do_GET and do_POST, covering /api/ping and the static branch as well as the routes; refuse a non-loopback Host and a foreign Origin.
- [ ] 4. Rewrite the --serve section of SECURITY.md against the code as it then stands: the port rule, the token's guarantee, the cross-origin answer, and the directory-listing behaviour once the next step lands.
- [ ] 5. Add the containment condition to prune.candidates and confirm both prune and prune --dry-run survive a report pointing outside the project, with the file intact.
- [ ] 6. Refuse directory requests under the served root, and write on every /api/events poll so a gone peer is detected on the next turn.
- [ ] 7. Hold the engine Popen so the existing BaseException path kills it before unlinking the report, and record in the docstring what an interrupt leaves.
- [ ] 8. Rename the fallback resolution rule and correct the paths docstring, following the name through the doctor output and the locale catalogues.
- [ ] 9. Add one check per change to scripts/selfcheck.py with its thin pytest wrapper in tests/, following the shape the existing checks use.
- [ ] 10. Run make check and make logics, plus scripts/viewer_smoke.py in served mode; run scripts/fixture_check.py if a Blender is available and say so if it is not.
- [ ] 11. Record in the task which findings were closed by which change, and which of req_012's context notes were confirmed or contradicted along the way.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_056_refuse_a_served_viewer_request_that_did_not_come_from_its_own_page`
- `item_057_keep_prune_inside_the_project_it_was_asked_to_prune`
- `item_058_stop_the_served_viewer_listing_work_and_holding_threads_for_absent_peers`
- `item_059_leave_nothing_running_and_nothing_mislabelled_after_an_interrupted_run`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_056_refuse_a_served_viewer_request_that_did_not_come_from_its_own_page`. Proof deferred to slice closeout.
- request-AC2 -> `item_056_refuse_a_served_viewer_request_that_did_not_come_from_its_own_page`. Proof deferred to slice closeout.
- request-AC8 -> `item_056_refuse_a_served_viewer_request_that_did_not_come_from_its_own_page`. Proof deferred to slice closeout.
- request-AC3 -> `item_057_keep_prune_inside_the_project_it_was_asked_to_prune`. Proof deferred to slice closeout.
- request-AC8 -> `item_057_keep_prune_inside_the_project_it_was_asked_to_prune`. Proof deferred to slice closeout.
- request-AC4 -> `item_058_stop_the_served_viewer_listing_work_and_holding_threads_for_absent_peers`. Proof deferred to slice closeout.
- request-AC5 -> `item_058_stop_the_served_viewer_listing_work_and_holding_threads_for_absent_peers`. Proof deferred to slice closeout.
- request-AC8 -> `item_058_stop_the_served_viewer_listing_work_and_holding_threads_for_absent_peers`. Proof deferred to slice closeout.
- request-AC6 -> `item_059_leave_nothing_running_and_nothing_mislabelled_after_an_interrupted_run`. Proof deferred to slice closeout.
- request-AC7 -> `item_059_leave_nothing_running_and_nothing_mislabelled_after_an_interrupted_run`. Proof deferred to slice closeout.
- request-AC8 -> `item_059_leave_nothing_running_and_nothing_mislabelled_after_an_interrupted_run`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_013_make_the_served_viewer_prune_and_project_resolution_behave_the_way_they_are_documented`
- Product brief(s): `prod_013_a_host_boundary_that_matches_its_own_documentation`
- Architecture decision(s): (none yet)

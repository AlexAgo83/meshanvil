## task_028_deliver_a_first_run_path_a_fresh_installation_can_walk - Deliver a first-run path a fresh installation can walk
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
- Summary: Implementation plan for the first-run request, ordered so the check that catches installation defects lands before the slices that could introduce them.
- Keywords: install check, demo command, doctor side effect, README install route
- Use when: delivering req_015 or coordinating its four backlog slices.
- Skip when: working on the agent-facing JSON contract, which is a separate request.

# Context
- Coordinate the AC-aware split backlog items without implementing them directly.
- The request was written from a real walkthrough: the wheel built, installed into a clean venv, and the README followed line by line. Two defects found on that walk are already fixed; these four slices are what it did not cover.
- PyPI was decided against for a pre-1.0 tool. the README slice below documents the route that works today; claiming the name is deferred to 1.0.

# Plan
- [ ] 1. `item_067` first: the install check is what catches this whole class of defect, and every slice below is safer once a target fails when the installed command stops working.
- [ ] 2. `item_070`: correct the README installation line. One line, and it is the first command a new reader runs.
- [ ] 3. `item_069`: move directory creation out of `doctor` and into `run`, with the refusal path adjusted in the same change.
- [ ] 4. `item_068`: add the demo command last, once `doctor` no longer creates directories under it and the install check can exercise it.
- [ ] 5. Run `make check`, `make install-check`, `make package`, Logics lint, audit and flow validate.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and validation pass.

# Backlog
- `item_067_install_the_wheel_and_run_the_command_in_a_clean_environment`
- `item_068_give_a_fresh_installation_a_subject_it_can_generate_itself`
- `item_069_let_doctor_read_init_prepare_and_run_create`
- `item_070_point_the_readme_installation_at_a_route_that_works_today`

# Definition of Done (DoD)
- [ ] Generated backlog slices are linked and ready for implementation.
- [ ] Slice ownership and next action are clear.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009 without automatic commits or one commit per micro-step.

# AC Traceability
- request-AC1 -> `item_070_point_the_readme_installation_at_a_route_that_works_today`. Proof deferred to slice closeout.
- request-AC2 -> `item_068_give_a_fresh_installation_a_subject_it_can_generate_itself`. Proof deferred to slice closeout.
- request-AC3 -> `item_068_give_a_fresh_installation_a_subject_it_can_generate_itself`. Proof deferred to slice closeout.
- request-AC4 -> `item_069_let_doctor_read_init_prepare_and_run_create`. Proof deferred to slice closeout.
- request-AC5 -> `item_067_install_the_wheel_and_run_the_command_in_a_clean_environment`. Proof deferred to slice closeout.
- request-AC6 -> `item_067_install_the_wheel_and_run_the_command_in_a_clean_environment`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_015_make_a_fresh_installation_reach_its_first_report`
- Product brief(s): (none yet)
- Architecture decision(s): (none yet)

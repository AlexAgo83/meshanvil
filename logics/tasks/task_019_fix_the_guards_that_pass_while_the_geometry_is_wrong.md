## task_019_fix_the_guards_that_pass_while_the_geometry_is_wrong - Fix the guards that pass while the geometry is wrong
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 66%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: Claude
> Indicators reviewed: 2026-08-22 14:02:34

# AI Context
- Summary: Orchestrates three corrections to checks that report what they did not measure, each reproduced on the asset that exposed it, each left with a check that fails if it regresses.
- Keywords: orchestration, thin feature, walling tolerance, mesh import, regression coverage
- Use when: planning or sequencing the guard fixes, or checking what remains before closeout.
- Skip when: the work is about what the demonstration shows rather than what an operation measures.
# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Reproduce each of the three on the assets that exposed them and keep the numbers in the task notes.
- [ ] 2. Replace the smallest-object measure with a thin-feature estimate and warn against the voxel about to be used.
- [ ] 3. Make the walling decision proportional and record what it decided per object.
- [ ] 4. Add the mesh import operation and confirm a chain can start from it.
- [ ] 5. Extend the fixture check so each guard fails when it goes back to reporting what it does not measure.
- [ ] 6. Confirm the vehicle demonstration is unchanged, then run make check, the fixture check and the browser smoke before closeout.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_029_measure_the_thinnest_feature_not_the_smallest_object`
- `item_030_decide_walling_on_how_open_a_body_is`
- `item_031_let_a_mesh_source_enter_the_pipeline`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_029_measure_the_thinnest_feature_not_the_smallest_object`. Proof deferred to slice closeout.
- request-AC2 -> `item_029_measure_the_thinnest_feature_not_the_smallest_object`. Proof deferred to slice closeout.
- request-AC6 -> `item_029_measure_the_thinnest_feature_not_the_smallest_object`. Proof deferred to slice closeout.
- request-AC3 -> `item_030_decide_walling_on_how_open_a_body_is`. Proof deferred to slice closeout.
- request-AC4 -> `item_030_decide_walling_on_how_open_a_body_is`. Proof deferred to slice closeout.
- request-AC6 -> `item_030_decide_walling_on_how_open_a_body_is`. Proof deferred to slice closeout.
- request-AC5 -> `item_031_let_a_mesh_source_enter_the_pipeline`. Proof deferred to slice closeout.
- request-AC6 -> `item_031_let_a_mesh_source_enter_the_pipeline`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_005_fix_the_guards_that_pass_while_the_geometry_is_wrong`
- Product brief(s): `prod_006_guards_that_measure_what_they_claim`
- Architecture decision(s): (none yet)

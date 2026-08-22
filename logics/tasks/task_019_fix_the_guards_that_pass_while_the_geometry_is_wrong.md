## task_019_fix_the_guards_that_pass_while_the_geometry_is_wrong - Fix the guards that pass while the geometry is wrong
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
> Indicators reviewed: 2026-08-22 14:31:42

# AI Context
- Summary: Orchestrates three corrections to checks that report what they did not measure, each reproduced on the asset that exposed it, each left with a check that fails if it regresses.
- Keywords: orchestration, thin feature, walling tolerance, mesh import, regression coverage
- Use when: planning or sequencing the guard fixes, or checking what remains before closeout.
- Skip when: the work is about what the demonstration shows rather than what an operation measures.
# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 1. Reproduce each of the three on the assets that exposed them and keep the numbers in the task notes.
- [x] 2. Replace the smallest-object measure with a thin-feature estimate and warn against the voxel about to be used.
- [x] 3. Make the walling decision proportional and record what it decided per object.
- [x] 4. Add the mesh import operation and confirm a chain can start from it.
- [x] 5. Extend the fixture check so each guard fails when it goes back to reporting what it does not measure.
- [x] 6. Confirm the vehicle demonstration is unchanged, then run make check, the fixture check and the browser smoke before closeout.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_029_measure_the_thinnest_feature_not_the_smallest_object`
- `item_030_decide_walling_on_how_open_a_body_is`
- `item_031_let_a_mesh_source_enter_the_pipeline`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented in c90cf6a (walling by openness share), 74825df (thin-feature measure by ray cast), 034f737 (OBJ/STL/PLY import) and 1a93084 (fixture coverage). Validated with: python3 scripts/fixture_check.py, make check, python3 scripts/viewer_smoke.py -- all passed; each guard negative-tested by reverting it. Source: `1a93084`
- request-AC2 -> This task. Proof: Implemented in c90cf6a (walling by openness share), 74825df (thin-feature measure by ray cast), 034f737 (OBJ/STL/PLY import) and 1a93084 (fixture coverage). Validated with: python3 scripts/fixture_check.py, make check, python3 scripts/viewer_smoke.py -- all passed; each guard negative-tested by reverting it. Source: `1a93084`
- request-AC6 -> This task. Proof: Implemented in c90cf6a (walling by openness share), 74825df (thin-feature measure by ray cast), 034f737 (OBJ/STL/PLY import) and 1a93084 (fixture coverage). Validated with: python3 scripts/fixture_check.py, make check, python3 scripts/viewer_smoke.py -- all passed; each guard negative-tested by reverting it. Source: `1a93084`
- request-AC3 -> This task. Proof: Implemented in c90cf6a (walling by openness share), 74825df (thin-feature measure by ray cast), 034f737 (OBJ/STL/PLY import) and 1a93084 (fixture coverage). Validated with: python3 scripts/fixture_check.py, make check, python3 scripts/viewer_smoke.py -- all passed; each guard negative-tested by reverting it. Source: `1a93084`
- request-AC4 -> This task. Proof: Implemented in c90cf6a (walling by openness share), 74825df (thin-feature measure by ray cast), 034f737 (OBJ/STL/PLY import) and 1a93084 (fixture coverage). Validated with: python3 scripts/fixture_check.py, make check, python3 scripts/viewer_smoke.py -- all passed; each guard negative-tested by reverting it. Source: `1a93084`
- request-AC6 -> This task. Proof: Implemented in c90cf6a (walling by openness share), 74825df (thin-feature measure by ray cast), 034f737 (OBJ/STL/PLY import) and 1a93084 (fixture coverage). Validated with: python3 scripts/fixture_check.py, make check, python3 scripts/viewer_smoke.py -- all passed; each guard negative-tested by reverting it. Source: `1a93084`
- request-AC5 -> This task. Proof: Implemented in c90cf6a (walling by openness share), 74825df (thin-feature measure by ray cast), 034f737 (OBJ/STL/PLY import) and 1a93084 (fixture coverage). Validated with: python3 scripts/fixture_check.py, make check, python3 scripts/viewer_smoke.py -- all passed; each guard negative-tested by reverting it. Source: `1a93084`
- request-AC6 -> This task. Proof: Implemented in c90cf6a (walling by openness share), 74825df (thin-feature measure by ray cast), 034f737 (OBJ/STL/PLY import) and 1a93084 (fixture coverage). Validated with: python3 scripts/fixture_check.py, make check, python3 scripts/viewer_smoke.py -- all passed; each guard negative-tested by reverting it. Source: `1a93084`

# Validation
- (no validation recorded yet)
- command: `python3 scripts/fixture_check.py && make check && python3 scripts/viewer_smoke.py` | result: passed | date: 2026-08-22
- Finish workflow executed on 2026-08-22.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-22.
- Linked backlog item(s): `item_029_measure_the_thinnest_feature_not_the_smallest_object`, `item_030_decide_walling_on_how_open_a_body_is`, `item_031_let_a_mesh_source_enter_the_pipeline`
- Related request(s): `req_005_fix_the_guards_that_pass_while_the_geometry_is_wrong`

# Links
- Request: `req_005_fix_the_guards_that_pass_while_the_geometry_is_wrong`
- Product brief(s): `prod_006_guards_that_measure_what_they_claim`
- Architecture decision(s): (none yet)

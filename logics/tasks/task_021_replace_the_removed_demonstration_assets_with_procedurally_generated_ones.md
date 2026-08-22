## task_021_replace_the_removed_demonstration_assets_with_procedurally_generated_ones - Replace the removed demonstration assets with procedurally generated ones
> From version: 0.1.0
> Schema version: 1.0
> Status: In progress
> Understanding: 90%
> Confidence: 85%
> Progress: 0%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Owner: Claude
> Indicators reviewed: 2026-08-22 19:01:53

# AI Context
- Summary: Orchestrates building both procedural generators, wiring them as the no-argument default into the two build scripts, and re-verifying the same branch lessons hold on the generated subjects.
- Keywords: orchestration, procedural generation, no donor file, verified not asserted
- Use when: planning or sequencing this slice, or checking what remains before closeout.
- Skip when: the work is about a chain's operations rather than the subject it runs on.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Write tools/make_demo_vehicle.py: a primitive-built body shell, mirrored wheels, a coincident duplicate. Verify by running the real chain, not by inspection.
- [ ] 2. Write tools/make_demo_figure.py: a primitive-built standing figure, closed by construction, with a finger thin enough to trigger the thin-feature guard at print scale. Verify the same way.
- [ ] 3. Wire both into build_demo_chain.sh and build_figurine_chain.sh as the no-argument default.
- [ ] 4. Update README's Demonstration data section and both scripts' comments to describe what was actually measured, including where the vehicle's interior part is only mostly hidden.
- [ ] 5. Rebuild both demonstration projects from scratch and confirm the same branch behaviour (destructive remesh caught; thin-feature guard discriminating) holds.
- [ ] 6. Run make check, the fixture check and the browser smoke before closeout.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_034_generate_a_vehicle_scale_subject_that_carries_the_same_defects`
- `item_035_generate_a_figurine_scale_subject_with_a_real_thin_feature`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_034_generate_a_vehicle_scale_subject_that_carries_the_same_defects`. Proof deferred to slice closeout.
- request-AC2 -> `item_034_generate_a_vehicle_scale_subject_that_carries_the_same_defects`. Proof deferred to slice closeout.
- request-AC4 -> `item_034_generate_a_vehicle_scale_subject_that_carries_the_same_defects`. Proof deferred to slice closeout.
- request-AC5 -> `item_034_generate_a_vehicle_scale_subject_that_carries_the_same_defects`. Proof deferred to slice closeout.
- request-AC3 -> `item_035_generate_a_figurine_scale_subject_with_a_real_thin_feature`. Proof deferred to slice closeout.
- request-AC4 -> `item_035_generate_a_figurine_scale_subject_with_a_real_thin_feature`. Proof deferred to slice closeout.
- request-AC5 -> `item_035_generate_a_figurine_scale_subject_with_a_real_thin_feature`. Proof deferred to slice closeout.
- request-AC6 -> `item_035_generate_a_figurine_scale_subject_with_a_real_thin_feature`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_007_replace_the_removed_demonstration_assets_with_procedurally_generated_ones`
- Product brief(s): `prod_008_demonstrations_that_own_every_asset_they_run_on`
- Architecture decision(s): (none yet)

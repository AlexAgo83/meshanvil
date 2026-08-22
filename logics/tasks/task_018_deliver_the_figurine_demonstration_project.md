## task_018_deliver_the_figurine_demonstration_project - Deliver the figurine demonstration project
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
> Indicators reviewed: 2026-08-22 15:13:22

# AI Context
- Summary: Orchestrates the second demonstration: reducing and recording the subject, giving it a project, running a chain where the sweeps stay silent, and branching the remesh at two fractions of the subject.
- Keywords: orchestration, figurine, second project, negative control, voxel branch, documentation
- Use when: planning or sequencing the figurine demonstration, or checking what remains before closeout.
- Skip when: the work is a guard fix, which belongs to the other task.
# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 1. Confirm multi-project workspaces are in place, since two demonstrations cannot share one work directory.
- [x] 2. Reduce the subject with the strip tool and write its provenance record.
- [x] 3. Create the project and its build script, mirroring the vehicle one.
- [x] 4. Run the sweep, the size decision and the visibility pass, and check each result reads as deliberate.
- [x] 5. Add the two-voxel branch and confirm both report ok while the renders differ.
- [x] 6. Write the lesson into the documentation next to the demonstration section.
- [x] 7. Run make check, the fixture check, the browser smoke and both demonstration builds before closeout.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_026_ship_the_figurine_subject_as_its_own_demonstration_project`
- `item_027_build_the_figurine_chain_around_a_sound_subject_and_a_size_decision`
- `item_028_branch_the_remesh_at_two_fractions_of_the_subject`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented in 7c3c8f5: fixtures/demo_figure.blend shipped with provenance, both demonstrations rebased as sibling projects under work/demo/, tools/build_figurine_chain.sh added, README lesson written. Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh and tools/build_figurine_chain.sh -- all passed. Measured: scan_defects reports no finding on the sound subject; 0.5 mm is 3.0 voxels across a 1.501 mm feature and 1.5 mm is 1.0, both reporting ok. Source: `7c3c8f5`
- request-AC7 -> This task. Proof: Implemented in 7c3c8f5: fixtures/demo_figure.blend shipped with provenance, both demonstrations rebased as sibling projects under work/demo/, tools/build_figurine_chain.sh added, README lesson written. Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh and tools/build_figurine_chain.sh -- all passed. Measured: scan_defects reports no finding on the sound subject; 0.5 mm is 3.0 voxels across a 1.501 mm feature and 1.5 mm is 1.0, both reporting ok. Source: `7c3c8f5`
- request-AC2 -> This task. Proof: Implemented in 7c3c8f5: fixtures/demo_figure.blend shipped with provenance, both demonstrations rebased as sibling projects under work/demo/, tools/build_figurine_chain.sh added, README lesson written. Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh and tools/build_figurine_chain.sh -- all passed. Measured: scan_defects reports no finding on the sound subject; 0.5 mm is 3.0 voxels across a 1.501 mm feature and 1.5 mm is 1.0, both reporting ok. Source: `7c3c8f5`
- request-AC3 -> This task. Proof: Implemented in 7c3c8f5: fixtures/demo_figure.blend shipped with provenance, both demonstrations rebased as sibling projects under work/demo/, tools/build_figurine_chain.sh added, README lesson written. Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh and tools/build_figurine_chain.sh -- all passed. Measured: scan_defects reports no finding on the sound subject; 0.5 mm is 3.0 voxels across a 1.501 mm feature and 1.5 mm is 1.0, both reporting ok. Source: `7c3c8f5`
- request-AC6 -> This task. Proof: Implemented in 7c3c8f5: fixtures/demo_figure.blend shipped with provenance, both demonstrations rebased as sibling projects under work/demo/, tools/build_figurine_chain.sh added, README lesson written. Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh and tools/build_figurine_chain.sh -- all passed. Measured: scan_defects reports no finding on the sound subject; 0.5 mm is 3.0 voxels across a 1.501 mm feature and 1.5 mm is 1.0, both reporting ok. Source: `7c3c8f5`
- request-AC4 -> This task. Proof: Implemented in 7c3c8f5: fixtures/demo_figure.blend shipped with provenance, both demonstrations rebased as sibling projects under work/demo/, tools/build_figurine_chain.sh added, README lesson written. Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh and tools/build_figurine_chain.sh -- all passed. Measured: scan_defects reports no finding on the sound subject; 0.5 mm is 3.0 voxels across a 1.501 mm feature and 1.5 mm is 1.0, both reporting ok. Source: `7c3c8f5`
- request-AC5 -> This task. Proof: Implemented in 7c3c8f5: fixtures/demo_figure.blend shipped with provenance, both demonstrations rebased as sibling projects under work/demo/, tools/build_figurine_chain.sh added, README lesson written. Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh and tools/build_figurine_chain.sh -- all passed. Measured: scan_defects reports no finding on the sound subject; 0.5 mm is 3.0 voxels across a 1.501 mm feature and 1.5 mm is 1.0, both reporting ok. Source: `7c3c8f5`

# Validation
- (no validation recorded yet)
- command: `make check && python3 scripts/fixture_check.py && python3 scripts/viewer_smoke.py && tools/build_demo_chain.sh && tools/build_figurine_chain.sh` | result: passed | date: 2026-08-22
- Finish workflow executed on 2026-08-22.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-22.
- Linked backlog item(s): `item_026_ship_the_figurine_subject_as_its_own_demonstration_project`, `item_027_build_the_figurine_chain_around_a_sound_subject_and_a_size_decision`, `item_028_branch_the_remesh_at_two_fractions_of_the_subject`
- Related request(s): `req_004_demonstrate_on_a_clean_organic_subject_what_the_vehicle_chain_cannot_show`

# Links
- Request: `req_004_demonstrate_on_a_clean_organic_subject_what_the_vehicle_chain_cannot_show`
- Product brief(s): `prod_005_demonstrations_that_show_the_checks_discriminating`
- Architecture decision(s): (none yet)

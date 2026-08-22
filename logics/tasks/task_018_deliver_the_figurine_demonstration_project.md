## task_018_deliver_the_figurine_demonstration_project - Deliver the figurine demonstration project
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
- Summary: Orchestrates the second demonstration: reducing and recording the subject, giving it a project, running a chain where the sweeps stay silent, and branching the remesh at two fractions of the subject.
- Keywords: orchestration, figurine, second project, negative control, voxel branch, documentation
- Use when: planning or sequencing the figurine demonstration, or checking what remains before closeout.
- Skip when: the work is a guard fix, which belongs to the other task.
# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Confirm multi-project workspaces are in place, since two demonstrations cannot share one work directory.
- [ ] 2. Reduce the subject with the strip tool and write its provenance record.
- [ ] 3. Create the project and its build script, mirroring the vehicle one.
- [ ] 4. Run the sweep, the size decision and the visibility pass, and check each result reads as deliberate.
- [ ] 5. Add the two-voxel branch and confirm both report ok while the renders differ.
- [ ] 6. Write the lesson into the documentation next to the demonstration section.
- [ ] 7. Run make check, the fixture check, the browser smoke and both demonstration builds before closeout.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_026_ship_the_figurine_subject_as_its_own_demonstration_project`
- `item_027_build_the_figurine_chain_around_a_sound_subject_and_a_size_decision`
- `item_028_branch_the_remesh_at_two_fractions_of_the_subject`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_026_ship_the_figurine_subject_as_its_own_demonstration_project`. Proof deferred to slice closeout.
- request-AC7 -> `item_026_ship_the_figurine_subject_as_its_own_demonstration_project`. Proof deferred to slice closeout.
- request-AC2 -> `item_027_build_the_figurine_chain_around_a_sound_subject_and_a_size_decision`. Proof deferred to slice closeout.
- request-AC3 -> `item_027_build_the_figurine_chain_around_a_sound_subject_and_a_size_decision`. Proof deferred to slice closeout.
- request-AC6 -> `item_027_build_the_figurine_chain_around_a_sound_subject_and_a_size_decision`. Proof deferred to slice closeout.
- request-AC4 -> `item_028_branch_the_remesh_at_two_fractions_of_the_subject`. Proof deferred to slice closeout.
- request-AC5 -> `item_028_branch_the_remesh_at_two_fractions_of_the_subject`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_004_demonstrate_on_a_clean_organic_subject_what_the_vehicle_chain_cannot_show`
- Product brief(s): `prod_005_demonstrations_that_show_the_checks_discriminating`
- Architecture decision(s): (none yet)

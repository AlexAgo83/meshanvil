## task_017_deliver_multi_project_workspaces_and_the_viewer_switcher - Deliver multi-project workspaces and the viewer switcher
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
- Summary: Orchestrates the split of code location from work location, per-project identity, parentage and retention, the project switcher in the viewer, and the coverage that keeps the current single-directory setup working.
- Keywords: orchestration, code root, work root, project resolution, namespace scoping, viewer switcher, migration
- Use when: planning or sequencing the multi-project work, or checking what remains before closeout.
- Skip when: the work is a single isolated fix inside one of the backlog items.
# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [ ] 1. Inventory every use of the current root and record, per call site, whether it meant code or work; keep that list in the task notes.
- [ ] 2. Introduce the two roots and move the call sites, keeping the work root defaulting to the installation.
- [ ] 3. Carry both roots in the job file and confirm an engine script imports the package and writes renders correctly from a foreign work root.
- [ ] 4. Add project resolution by marker walk-up with an explicit override, and the command that creates a project.
- [ ] 5. Scope identity allocation, fingerprint parentage and prune retention to the active project.
- [ ] 6. Surface the active project in the setup check, the top bar and the status bar.
- [ ] 7. Generate the project list into the viewer data and implement the switcher as a read-only selection.
- [ ] 8. Extend the self-check with a two-project isolation case and the browser smoke with the switcher.
- [ ] 9. Run make check, the fixture check, the browser smoke and the demo chain before closeout.
- [ ] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [ ] Keep commit creation under operator control; do not force one commit per micro-step.
- [ ] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_021_split_the_code_root_from_the_work_root`
- `item_022_resolve_the_active_project_without_an_invisible_setting`
- `item_023_scope_identity_parentage_and_retention_to_one_project`
- `item_024_add_a_project_switcher_to_the_viewer`
- `item_025_prove_the_isolation_and_keep_the_current_setup_working`

# Definition of Done (DoD)
- [ ] Generated request, product, backlog, and task docs are present.
- [ ] Context-pack handoff is available when requested.
- [ ] Validation passes.
- [ ] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> `item_021_split_the_code_root_from_the_work_root`. Proof deferred to slice closeout.
- request-AC6 -> `item_021_split_the_code_root_from_the_work_root`. Proof deferred to slice closeout.
- request-AC2 -> `item_022_resolve_the_active_project_without_an_invisible_setting`. Proof deferred to slice closeout.
- request-AC6 -> `item_022_resolve_the_active_project_without_an_invisible_setting`. Proof deferred to slice closeout.
- request-AC7 -> `item_022_resolve_the_active_project_without_an_invisible_setting`. Proof deferred to slice closeout.
- request-AC3 -> `item_023_scope_identity_parentage_and_retention_to_one_project`. Proof deferred to slice closeout.
- request-AC6 -> `item_023_scope_identity_parentage_and_retention_to_one_project`. Proof deferred to slice closeout.
- request-AC4 -> `item_024_add_a_project_switcher_to_the_viewer`. Proof deferred to slice closeout.
- request-AC5 -> `item_024_add_a_project_switcher_to_the_viewer`. Proof deferred to slice closeout.
- request-AC6 -> `item_025_prove_the_isolation_and_keep_the_current_setup_working`. Proof deferred to slice closeout.
- request-AC8 -> `item_025_prove_the_isolation_and_keep_the_current_setup_working`. Proof deferred to slice closeout.

# Validation
- (no validation recorded yet)

# Report
- Not started.

# Links
- Request: `req_003_hold_several_model_projects_side_by_side_and_switch_between_them`
- Product brief(s): `prod_004_multi_project_operator_workspaces`
- Architecture decision(s): (none yet)

## task_017_deliver_multi_project_workspaces_and_the_viewer_switcher - Deliver multi-project workspaces and the viewer switcher
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
> Indicators reviewed: 2026-08-22 15:00:07

# AI Context
- Summary: Orchestrates the split of code location from work location, per-project identity, parentage and retention, the project switcher in the viewer, and the coverage that keeps the current single-directory setup working.
- Keywords: orchestration, code root, work root, project resolution, namespace scoping, viewer switcher, migration
- Use when: planning or sequencing the multi-project work, or checking what remains before closeout.
- Skip when: the work is a single isolated fix inside one of the backlog items.
# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 1. Inventory every use of the current root and record, per call site, whether it meant code or work; keep that list in the task notes.
- [x] 2. Introduce the two roots and move the call sites, keeping the work root defaulting to the installation.
- [x] 3. Carry both roots in the job file and confirm an engine script imports the package and writes renders correctly from a foreign work root.
- [x] 4. Add project resolution by marker walk-up with an explicit override, and the command that creates a project.
- [x] 5. Scope identity allocation, fingerprint parentage and prune retention to the active project.
- [x] 6. Surface the active project in the setup check, the top bar and the status bar.
- [x] 7. Generate the project list into the viewer data and implement the switcher as a read-only selection.
- [x] 8. Extend the self-check with a two-project isolation case and the browser smoke with the switcher.
- [x] 9. Run make check, the fixture check, the browser smoke and the demo chain before closeout.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_021_split_the_code_root_from_the_work_root`
- `item_022_resolve_the_active_project_without_an_invisible_setting`
- `item_023_scope_identity_parentage_and_retention_to_one_project`
- `item_024_add_a_project_switcher_to_the_viewer`
- `item_025_prove_the_isolation_and_keep_the_current_setup_working`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC6 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC2 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC6 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC7 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC3 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC6 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC4 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC5 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC6 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`
- request-AC8 -> This task. Proof: Implemented in cd5ae1a (code root split from work root, both carried in the job), 03df22e (marker walk-up, meshanvil init, doctor visibility), 58ebb14 (two-project isolation in the self-check), 3f1bdfd (viewer project switcher) and 543e05b (project named in the status bar, splash and README). Validated with: make check, python3 scripts/fixture_check.py, python3 scripts/viewer_smoke.py, tools/build_demo_chain.sh -- all passed. Isolation proven on two real projects: identity restarted at 001, renders stayed in their project, the installation kept its eleven reports. Source: `543e05b`

# Validation
- (no validation recorded yet)
- command: `make check && python3 scripts/fixture_check.py && python3 scripts/viewer_smoke.py && tools/build_demo_chain.sh` | result: passed | date: 2026-08-22
- Finish workflow executed on 2026-08-22.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-22.
- Linked backlog item(s): `item_021_split_the_code_root_from_the_work_root`, `item_022_resolve_the_active_project_without_an_invisible_setting`, `item_023_scope_identity_parentage_and_retention_to_one_project`, `item_024_add_a_project_switcher_to_the_viewer`, `item_025_prove_the_isolation_and_keep_the_current_setup_working`
- Related request(s): `req_003_hold_several_model_projects_side_by_side_and_switch_between_them`

# Links
- Request: `req_003_hold_several_model_projects_side_by_side_and_switch_between_them`
- Product brief(s): `prod_004_multi_project_operator_workspaces`
- Architecture decision(s): (none yet)

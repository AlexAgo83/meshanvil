## task_025_deliver_an_installable_meshanvil - Deliver an installable meshanvil
> From version: 0.1.0
> Schema version: 1.0
> Status: Done
> Understanding: 90%
> Confidence: 85%
> Progress: 100%
> Complexity: Medium
> Theme: Implementation delivery
> Reminder: Update status/understanding/confidence/progress and linked request/backlog references when you edit this doc.
> Indicators reviewed: 2026-08-23 02:00:17
> Owner: codex

# AI Context
- Summary: Sequences the packaging: declare the package, unify asset resolution, verify the built package, repoint the viewer's subprocess, settle the runbook question, then the release ADR and procedure.
- Keywords: orchestration, packaging, asset resolution, release procedure, clean-environment verification
- Use when: Picking up or ordering the work of req_011.
- Skip when: Looking for what any one slice must satisfy -- the backlog items hold that.

# Context
- Orchestrate the scaffolded request chain and keep sibling implementation slices linked.

# Plan
- [x] 1. 1. Declare the package, add the console entry point, and single-source the version.
- [x] 2. 2. Replace the repository-root lookup with one repo-first resolution rule and declare every asset directory in the package.
- [x] 3. 3. Add the build-time check that a built package carries every asset the tool reads.
- [x] 4. 4. Point the viewer's closed command set at the installed entry point, confirming adr_007's guarantees are untouched.
- [x] 5. 5. Decide and implement what an installed tool offers in place of this repository's corpus.
- [x] 6. 6. Record the ADR superseding `No publication yet`, and make build, verify and release repeatable commands with a dry run.
- [x] 7. 7. Rewrite the README's installation section: engine requirement first, install command, contributor route kept.
- [x] 8. 8. Install the built package into a clean environment and run a full operation and the viewer from it; re-run make check and the smoke suites from a clone before closeout.
- [x] ADR 009 checkpoint: update affected Logics docs during each meaningful wave and leave the repo commit-ready.
- [x] Keep commit creation under operator control; do not force one commit per micro-step.
- [x] GATE: do not close until lint, audit, and scaffold validation pass.

# Backlog
- `item_051_declare_the_package_and_give_the_tool_a_real_entry_point`
- `item_052_resolve_every_runtime_asset_the_same_way_from_a_tree_or_a_package`
- `item_053_run_the_viewer_s_closed_command_set_through_the_installed_entry_point`
- `item_054_decide_what_an_installed_meshanvil_offers_in_place_of_this_repository_s_corpus`
- `item_055_make_releasing_a_procedure_and_state_what_was_measured`

# Definition of Done (DoD)
- [x] Generated request, product, backlog, and task docs are present.
- [x] Context-pack handoff is available when requested.
- [x] Validation passes.
- [x] Meaningful waves followed ADR 009: affected docs updated and the repo left commit-ready without automatic commits.

# AC Traceability
- request-AC1 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC2 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC6 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC11 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC3 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC4 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC5 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC7 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC8 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC9 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`
- request-AC10 -> This task. Proof: Implemented package entry point, repo-first/package asset resolution, wheel asset/runtime dependency checks, installed viewer command execution, project-local runbooks, ADR/README release decision and dry-run procedure in commits baf6587, b95d7e5 and 4cc87e6. Verified with make release-dry-run, make viewer-smoke, flow validate task_025_deliver_an_installable_meshanvil, and a clean venv install from the built wheel that ran meshanvil --version, init, list, list_shells via Blender, and view --file --no-open. Source: `4cc87e6`

# Validation
- (no validation recorded yet)
- command: `clean venv install from dist/meshanvil-0.1.0-py3-none-any.whl; meshanvil --version; meshanvil init; meshanvil list; MESHANVIL_BLENDER=/Applications/Blender.app/Contents/MacOS/Blender meshanvil run list_shells work/out/demo_source.blend; meshanvil view --file --no-open` | result: passed | date: 2026-08-23
- Finish workflow executed on 2026-08-23.
- Linked backlog/request close verification passed.

# Report
- Not started.
- Finished on 2026-08-23.
- Linked backlog item(s): `item_051_declare_the_package_and_give_the_tool_a_real_entry_point`, `item_052_resolve_every_runtime_asset_the_same_way_from_a_tree_or_a_package`, `item_053_run_the_viewer_s_closed_command_set_through_the_installed_entry_point`, `item_054_decide_what_an_installed_meshanvil_offers_in_place_of_this_repository_s_corpus`, `item_055_make_releasing_a_procedure_and_state_what_was_measured`
- Related request(s): `req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone`

# Links
- Request: `req_011_make_meshanvil_an_installable_tool_instead_of_a_repository_you_clone`
- Product brief(s): `prod_012_a_tool_you_install_not_a_repository_you_clone`
- Architecture decision(s): (none yet)
